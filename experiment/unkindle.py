from third_party.ion import DrmIon,DrmIonVoucher
from io import BytesIO
from pathlib import Path

import re
import requests
import os
import shutil
import sys
from third_party.kfxlib.unpack_container import IonTextContainer

from yj_to_folder import KFX_CBZ
import amazon_api
import config

DEBUG = False

class Kindle:
    def __init__(self, asin, ignore_hdv = False, hdv_png = False):
        self.asin = asin
        self.session = requests.Session()
        self.ignore_hdv = ignore_hdv
        self.hdv_png = hdv_png

        print("Authenticating . . .")
        self.tokens = amazon_api.login(config.EMAIL, config.PASSWORD, config.DOMAIN)


    def decrypt_voucher(self, voucher_data):
        with BytesIO(voucher_data) as voucher_data_io:
            voucher = DrmIonVoucher(voucher_data_io, self.tokens["device_id"], "")
            voucher.parse()
            voucher.decryptvoucher()
        return voucher


    def decrypt_kfx(self, kfx_data):
        if kfx_data[:8] != b'\xeaDRMION\xee':
            return kfx_data

        with BytesIO() as decrypted_data:
            DrmIon(BytesIO(kfx_data[8:-8]), lambda name: self.drm_voucher).parse(decrypted_data)
            return decrypted_data.getvalue()


    def get_resource(self, resource):
        resp = self.session.send(
            amazon_api.signed_request(
                "GET",
                resource["endpoint"]["url"],
                asin = self.asin,
                tokens = self.tokens,
                request_id = resource["id"],
                request_type = resource["type"]
            )
        )

        filename = resource["id"]
        if resource["type"] == "DRM_VOUCHER":
            filename += ".ast"
        else:
            filename += ".kfx"

        return (resp.content, filename)


    def get_book(self):
        manifest_resp = self.session.send(
            amazon_api.signed_request(
                "GET", 
                config.API_MANIFEST_URL + self.asin,
                asin = self.asin,
                tokens = self.tokens,
                request_type="manifest"
            )
        )
        
        if DEBUG:
            for header in manifest_resp.request.headers:
                print(f"{header}:{manifest_resp.request.headers[header]}")

        if manifest_resp.status_code != 200:
            print("Could not acquire the manifest!")
            return False
        
        self.resources = manifest_resp.json()["resources"]

        drm_voucher = [resource for resource in self.resources if resource["type"] == "DRM_VOUCHER"][0]
        try:
            self.drm_voucher = self.decrypt_voucher(self.get_resource(drm_voucher)[0])
        except:
            print("Could not decrypt the drm voucher!")
            return False
        
        self.resources = [resource for resource in self.resources if resource["type"] not in ["DRM_VOUCHER", "KINDLE_USER_ANOT"]]

        total = 0
        for resource in self.resources:
            total += resource["size"]
        print(f"download size: {int(total/1024/1024)}MB")

        return True


    def download(self):
        cwd = os.getcwd()
        output_folder = os.path.join(cwd, "comix_out")
        Path(output_folder).mkdir(exist_ok=True)
        temp_folder = os.path.join(output_folder, self.asin + "_temp")
        Path(temp_folder).mkdir(exist_ok=True)

        i = 0
        for resource in self.resources[i:]:
            print(f"Downloading the book . . {int(i/len(self.resources)*100)}%\r", end="")

            res = self.get_resource(resource)
            with open(os.path.join(temp_folder, res[1]), "wb") as f:
                f.write(self.decrypt_kfx(res[0]))
            i += 1

        print("\nExtracting . . . ")

        book = KFX_CBZ(temp_folder, self.ignore_hdv, self.hdv_png)
        metadata = book.get_metadata()

        regex = r"\.|\?|\\|/|<|>|\"|'|%|\*|\&|\+|\-|\#|\!"
        self.release_name = re.sub(r"\s+", " ", re.sub(regex, '', metadata.title).replace(":", "-"))
        print(f"{self.asin} : {self.release_name}")

        content_folder = os.path.join(output_folder, self.release_name)
        Path(content_folder).mkdir(exist_ok=True)

        if DEBUG:
            with open(content_folder + ".ion", "wb") as f:
                f.write(IonTextContainer(book.symtab, fragments=book.fragments.filtered(omit_resources=True)).serialize())

        book.extract_to_folder(content_folder, f"{self.release_name} - p")

        if not DEBUG:
            shutil.rmtree(temp_folder)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage:\unkindle <asin>\n - Downloads the content for the specified asin\n") #kindle list\n - Lists all content associated with the current account")
        exit()
    
    #if sys.argv[1] == "list":
        #kindle = Kindle(None)
        #kindle.print_list()

    kindle = Kindle(sys.argv[1])
    if kindle.get_book():
        kindle.download()
