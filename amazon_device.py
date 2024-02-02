# Generate random device information for use with the Amazon api. Since acquiring highest
# quality books requires sending device information, sending random information is a good way
# to avoid fingerprinting 

import hashlib
import random
import secrets
import string

MANUFACTURERS = [
    "Asus", "Google", "HTC", "Huawei", "Motorola", "Nokia", "NVIDIA", "OPPO", "OnePlus", "Samsung", "Sony", "Xiaomi"
]
ANDROID_API_LEVELS = {
    9: 28,
    10: 29,
    11: 30,
    12: 31,
    13: 33,
    14: 34,
}

def get_random_string(length, uppercase=False):
    letters = string.ascii_uppercase if uppercase else string.ascii_lowercase
    letters += string.digits
    
    return ''.join(random.choice(letters) for i in range(length))

def get_random_amazon_device():
    device_id = secrets.token_hex(16)
    manufacturer = random.choice(MANUFACTURERS)
    name = get_random_string(random.randint(4, 10), uppercase=True)
    codename = get_random_string(random.randint(4, 6), uppercase=False)
        
    os_version = random.randint(9, 14) # Android OS version
    build_id = str(random.randint(100000, 99999999)) # 6-8 digits
        
    return {
        "device_id": device_id,
        "pid": hashlib.sha256(device_id.encode()).hexdigest()[23:31].upper(),
        "manufacturer": manufacturer,
        "name": name,
        "codename": codename,
        "name_full": f"{codename}/{manufacturer}/{name}",
        "os_version": os_version,
        "os_api": ANDROID_API_LEVELS[os_version],
        "build_id": build_id,
        "build_fingerprint": f"{manufacturer}/{codename}/{codename}:{os_version}/{build_id}/{str(random.randint(100000, 99999999))}:user/release-keys",
        "width": 2160,
        "height": 3840,
        "app_name": "com.amazon.kindle",
        "app_version": "1285671411",
        "device_type": "A1MPSLFC7L5AFK",
        "device_type2": "A2Y8LFC259B97P",
        "pfm": "A1F83G8C2ARO7P",
        "sw_version": "130050002"
    }

def get_capabilities(device):
    return {
        "capabilities": {
            "attributes": {
                "android.hardware.ram.normal": "true",
                "model": device["name"],
                "brand": device["manufacturer"],
                "build.id": device["build_id"],
                "deviceDisplayXDpi": "360.000",
                "build.fingerprint": device["build_fingerprint"],
                "deviceDensityClassification": "360",
                "sizeRangeLargest": f"{device['height']} , {device['height'] - 100}",
                "deviceDensityScaled": "2.0",
                "manufacturer": device["manufacturer"],
                "deviceScreenLayout": "SCREENLAYOUT_SIZE_XLARGE",
                "deviceTouchscreen": "TOUCHSCREEN_FINGER",
                "android.hardware.audio.output": "true",
                "display": device["build_id"],
                "build.supportedABIs": "arm64-v8a,armeabi-v7a,armeabi",
                "build.hardware": "qcom",
                "screenLayoutRaw": "1",
                "deviceDisplayYDpi": "360.000",
                "build.product": device["codename"],
                "build.device": device["codename"],
                "APILevel": str(device["os_api"],),
                "deviceDensityLogical": "2.0",
                "android.software.verified_boot": "true",
                "android.hardware.hardware_keystore": "true",
                "android.hardware.camera": "true",
                "android.hardware.touchscreen": "true",
                "releaseVersion": str(device["os_version"]),
                "android.hardware.camera.any": "true",
                "carrier": "unknown",
                "sizeRangeSmallest": f"{device['width']} , {device['width'] - 100}",
                "android.hardware.wifi": "true",
                "screenRealSize.height": str(device["height"]),
                "screenRealSize.width": str(device["width"]),
                "deviceDisplayPixelsHeight": str(device["height"]),
                "deviceDisplayPixelsWidth": str(device["width"])
            },
            "schema": "http://dcaps.amazon.com/schema/dcaps_android/1"
        },
        "client_version": "android.1"
    }
