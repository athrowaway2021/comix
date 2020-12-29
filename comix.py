from google.protobuf.message import DecodeError
from pathlib import Path

import google.protobuf
import io
import os
import requests
import sys
import pyzipper

import config
import comix_key
import comix_pb2

class Cmx:
    def __init__(self, item_id):
        self.session = requests.Session()
        self.item_id = int(item_id)
    
    
    def get_comic(self):
        download_form = {"auth_token": "lwa-|" + config.AUTH_TOKEN, "comic_format": "IPAD_PROVISIONAL_HD", "item_id": self.item_id }
        response = self.session.post(config.API_DOWNLOAD_URL, headers = config.API_HEADERS, data = download_form)
        
        response_proto = comix_pb2.ComicResponse()

        try:
            response_proto.ParseFromString(response.content)
        except DecodeError:
            print("Could not parse response protobuf . . .\nResponse data: " + response.text)
            return False

        if response_proto.error.errormsg != "":
            print(response_proto.error.errormsg)
            return False

        if response_proto.comic.comic_id == "" or len(response_proto.comic.book.pages) == 0:
            print("Could not acquire the content info")
            return False

        self.comic = response_proto.comic

        print(str(self.item_id) + " : " + self.comic.issue.title)

        return True


    def download(self):
        cwd = os.getcwd()
        output_folder = os.path.join(cwd, "comix_out")
        Path(output_folder).mkdir(exist_ok=True)
        content_folder = os.path.join(output_folder, str(self.item_id))
        Path(content_folder).mkdir(exist_ok=True)

        i = 0
        for page in self.comic.book.pages:
            print("\rDownloading page {0} . . .".format(str(i).zfill(3)), end='')
            for image in page.pageinfo.images:
                if image.type != image.Type.FULL:
                    continue
                image_key = comix_key.calculate_key(image.digest.data, self.item_id, self.comic.version, self.comic.issue.publisher.publisher_id, i)
                
                response = self.session.get(image.uri)
                with pyzipper.AESZipFile(io.BytesIO(response.content)) as zf:
                    zf.extractall(content_folder, pwd=image_key)
            i += 1
        print("\nDone!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: comix <item_id>")
        exit()
    
    cmx = Cmx(sys.argv[1])
    if cmx.get_comic():
        cmx.download()