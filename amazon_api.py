from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from urllib.parse import urlparse

import base64
import datetime
import getpass
import gzip
import hashlib
import hmac
import json
import os
import random
import requests
import secrets
import sys
import time
import uuid
import xmltodict

import amazon_device

SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
STATE_PATH = os.path.join(SCRIPT_PATH, "state.json")


def save_state(state):
    with open(STATE_PATH, "w") as f:
        f.write(json.dumps(state, indent=4))
def get_state():
    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, "r") as f:
            return json.loads(f.read())

def import_rsa_key(key):
    key = key.replace("\\n","").replace("-----BEGIN RSA PRIVATE KEY-----","").replace("-----END RSA PRIVATE KEY-----","").replace("-----BEGIN RSA PUBLIC KEY-----","").replace("-----END RSA PUBLIC KEY-----","")
    return RSA.import_key(base64.b64decode(key))


def get_auth_headers(domain):
    return {
        "x-amzn-identity-auth-domain": f"api.amazon.{domain}",
        "X-Amzn-RequestId": str(uuid.uuid4()),
    }

def get_api_headers(device):
    return {
        "accept": "*/*",
        "accept-encoding": "gzip",
        "accept-language": "en-US",
        "currenttransportmethod": "WiFi",
        "is_archived_items": "1",
        "user-agent": "okhttp/3.12.1",
        "x-adp-app-id": "KINDLE",
        "x-adp-app-sw": device["app_version"],
        "x-adp-attemptcount": "1",
        "x-adp-cor": "US",
        "x-adp-country": "US",
        "x-adp-lto": "0",
        "x-adp-pfm": device["pfm"],
        "x-adp-reason": "ArchivedItems",
        "x-adp-sw": device["app_version"],
        "x-adp-transport": "WiFi",
        "x-amzn-accept-type": "application/x.amzn.digital.deliverymanifest@1.0",
    }

def generate_frc(device):
    cookies = json.dumps({
        "ApplicationName": device["app_name"],
        "ApplicationVersion": device["app_version"],
        "DeviceOSVersion": device["build_fingerprint"],
        "DeviceName": device["name_full"],
        "ScreenWidthPixels": device["width"],
        "ThirdPartyDeviceId": device["device_id"],
        "FirstPartyDeviceId": device["device_id"],
        "ScreenHeightPixels": device["height"],
        "DeviceLanguage": "en-US",
        "TimeZone": "+00:00",
        "IpAddress": requests.get('https://ident.me/').text,
    })

    def pkcs7_pad(data):
        padsize = 16 - len(data) % 16
        return data + bytes([padsize]) * padsize

    compressed = gzip.compress(cookies.encode())
    
    key = PBKDF2(device["device_id"], b"AES/CBC/PKCS7Padding")
    iv = secrets.token_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pkcs7_pad(compressed))

    hmac_ = hmac.new(PBKDF2(device["device_id"], b"HmacSHA256"), iv + ciphertext, hashlib.sha256).digest()

    return base64.b64encode(b"\0" + hmac_[:8] + iv + ciphertext).decode()


def login(email, password, domain = "com"):
    state = get_state()
    if state:
        ret = refresh(state)
        if ret:
            print("Logged in with saved state")
            return ret
        else:
            print("Could not refresh saved state")
    
    print("Enter your Amazon credentials . . .")
    if not email:
        email = input("Email: ")
    if not password:
        password = getpass.getpass("Password: ")
        
    device = amazon_device.get_random_amazon_device()

    body = {
        "auth_data": {
            "use_global_authentication": "true",
            "user_id_password": {
                "password" : password,
                "user_id": email
            },
        },
        "registration_data": {
            "domain": "DeviceLegacy",
            "device_type": device["device_type"],
            "device_serial": device["device_id"],
            "app_name": device["app_name"],
            "app_version": device["app_version"],
            "device_model": device["name"],
            "os_version": device["build_fingerprint"],
            "software_version": device["sw_version"],
        },
        "requested_token_type": ["bearer","mac_dms","store_authentication_cookie","website_cookies"],
        "cookies": {
            "domain": f"amazon.{domain}",
            "website_cookies": []
        },
        "user_context_map": {
            "frc": generate_frc(device)
        },
        "device_metadata": {
            "device_os_family": "android",
            "device_type": device["device_type"],
            "device_serial": device["device_id"],
            "manufacturer": device["manufacturer"],
            "model": device["name"],
            "os_version": str(device["os_api"]),
            "product": device["codename"],
        },
        "requested_extensions": ["device_info","customer_info"]
    }

    response = requests.post(f"https://api.amazon.{domain}:443/auth/register", headers=get_auth_headers(domain), json=body)
    
    if response.status_code != 200:
        response = response.json()        
        if "challenge" in response["response"] and response["response"]["challenge"]["challenge_reason"] == "HandleOnWebView":
            print("Amazon needs to reconfirm your identity with 2FA. Please logout and login again in your browser.")
        return None
    
    response = response.json()
    try:
        state = {
            "name": hashlib.md5(email.encode()).hexdigest(), # to differentiate states from different accounts
            "domain": domain,
            "device": device,
            "access_token": response["response"]["success"]["tokens"]["bearer"]["access_token"],
            "refresh_token": response["response"]["success"]["tokens"]["bearer"]["refresh_token"],
            "device_private_key": response["response"]["success"]["tokens"]["mac_dms"]["device_private_key"],
            "adp_token": response["response"]["success"]["tokens"]["mac_dms"]["adp_token"],
        }
        return register_device(state)
    except Exception as e:
        print(e)
        return None


def refresh(state):
    body = {
        "app_name": state["device"]["app_name"],
        "app_version": state["device"]["app_version"],
        "source_token_type": "refresh_token",
        "source_token": state["refresh_token"],
        "requested_token_type": "access_token"
    }
    
    response_json = requests.post(f"https://api.amazon.com/auth/token", headers=get_auth_headers(state["domain"]), json=body).json()
    try:
        state["access_token"] = response_json["access_token"]
    except:
        print(json.dumps(response_json))
        return None
    return state


def signed_request(method, url, headers = None, body = None, asin = None, state = None, request_id = None, request_type = None):
    """
    modified from https://github.com/mkb79/Audible/blob/master/src/audible/auth.py
    """

    if not state:
        state = get_state()
    if not state:
        print("Could not retrieve auth state")
        return None
    elif "adp_token" not in state:
        print("Could not find the adp token in saved state")
        return None
    elif "device_private_key" not in state:
        print("Could not find the private key in saved state")
        return None

    if not request_id:
        request_id = str(uuid.uuid4())
    else:
        request_id += str(int(time.time())) + str(random.randint(100, 999))

    if not body:
        body = ""
    
    date = datetime.datetime.utcnow().isoformat("T")[:-7] + "Z"
    u = urlparse(url)
    path = f"{u.path}"
    if u.query != "":
        path += f"{u.params}?{u.query}"
    data = f"{method}\n{path}\n{date}\n{body}\n{state['adp_token']}"

    key = import_rsa_key(state["device_private_key"])
    signed_encoded = base64.b64encode(pkcs1_15.new(key).sign(SHA256.new(data.encode())))
    signature = f"{signed_encoded.decode()}:{date}"
        
    if not headers:
        headers = get_api_headers(state["device"])
    if asin:
        headers["x-adp-correlationid"] = f"{asin}-{int(time.time())}420.kindle.ebook"
    if request_type == "DRM_VOUCHER":
        headers["accept"] = "application/x-com.amazon.drm.Voucher@1.0"
        headers["x-amzn-accept-type"] = "application/x-com.amazon.drm.Voucher@1.0"
    elif request_type == "manifest":
        headers["accept"] = "application/json"
        headers["x-amzn-accept-type"] = "application/x.amzn.digital.deliverymanifest@1.0"

    headers.update({
        "x-adp-token": state["adp_token"],
        "x-adp-alg": "SHA256WithRSA:1.0",
        "x-adp-signature": signature,
        "X-Amzn-RequestId": request_id,
    })
    return requests.Request(method, url, headers, data=body).prepare()


def register_device(state = None):
    if not state:
        state = get_state()
    
    url = "https://firs-ta-g7g.amazon.com/FirsProxy/registerAssociatedDevice"
    headers = {
        "Content-Type": "text/xml",
        "Expect": "",
    }
    #secret = "AAAA"
    body = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><parameters><deviceType>{state['device']['device_type2']}</deviceType><deviceSerialNumber>{state['device']['device_id']}</deviceSerialNumber><pid>{state['device']['pid']}</pid><deregisterExisting>true</deregisterExisting><softwareVersion>{state['device']['app_version']}</softwareVersion><softwareComponentId>{state['device']['app_name']}</softwareComponentId></parameters></request>"
    resp = requests.Session().send(signed_request("POST", url, headers, body, state=state))
        
    if resp.status_code == 200:
        parsed_response = xmltodict.parse(resp.text)
        state["device_private_key"] = parsed_response["response"]["device_private_key"]
        state["adp_token"] = parsed_response["response"]["adp_token"]

    # register device capabilities to allow HD content
    body = json.dumps(amazon_device.get_capabilities(state["device"]))
    resp = requests.Session().send(signed_request("POST", "https://dcapsproxy-na.amazon.com/capabilities/register", body=body, state=state))
    
    save_state(state)
    return state


if __name__ == "__main__":
    arg_count = len(sys.argv)
    if arg_count != 4:
        print("usage: amazon_auth.py <email> <password> <domain>")
        print("domains: com, co.uk, co.jp, de")
        exit()
    
    state = login(sys.argv[1], sys.argv[2], sys.argv[3])
    
    if state == None:
        print("Could not login!")
    else:
        print(json.dumps(state))

