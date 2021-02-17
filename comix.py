from google.protobuf.message import DecodeError
from pathlib import Path

import google.protobuf
import io
import os
import pyzipper
import requests
import sys

import config
import comix_key
import comix_pb2

class Cmx:
    def __init__(self, item_id):
        self.session = requests.Session()
        if item_id:
            self.item_id = int(item_id)
    
    
    def get_issue_infos(self, ids):
        issues_form = {"auth_token": "lwa-|" + config.AUTH_TOKEN }
        i = 0
        for _id in ids:
            issues_form["ids[{0}]".format(i)] = _id
            i += 1

        response = self.session.post(config.API_ISSUE_URL, headers = config.API_HEADERS, data = issues_form)

        issues_proto = comix_pb2.IssueResponse()
        issues_proto.ParseFromString(response.content)

        infos = []
        for issue in issues_proto.issues.issues:
            # prevent invalid filenames by replacing illegal symbols
            release_name = issue.title.replace(":", "-").replace("+", "").replace("?", "").replace("!", "").replace("%", "").replace("*", "").replace("&", " ").replace("/", "").replace("#", "").replace("\\", "").replace("  ", " ")
            if issue.volume != "":
                release_name += " - v" + issue.volume.zfill(2)
            elif issue.issue != "":
                release_name += " - " + issue.issue.zfill(3)
            infos.append([issue.id, release_name]) 
        # return ids with names since the issues returned by the api are in a different order than requested
        return infos


    def get_comic(self):
        download_form = {"auth_token": "lwa-|" + config.AUTH_TOKEN, "comic_format": "IPAD_PROVISIONAL_HD", "item_id": self.item_id }
        response = self.session.post(config.API_DOWNLOAD_URL, headers = config.API_HEADERS, data = download_form)
        
        response_proto = comix_pb2.ComicResponse()

        try:
            response_proto.ParseFromString(response.content)
        except DecodeError:
            print("Could not parse response protobuf, dumping response . . .")
            f = open(str(self.item_id) + "_dump.bin", "wb")
            f.write(response.content)
            f.close()
            return False

        if response_proto.error.errormsg != "":
            print(response_proto.error.errormsg)
            return False

        if response_proto.comic.comic_id == "" or len(response_proto.comic.book.pages) == 0:
            print("Could not acquire the content info")
            return False

        self.comic = response_proto.comic
        self.release_name = self.get_issue_infos([self.item_id])[0][1]
        self.publisher_id = self.comic.issue.publisher.publisher_id
        if publisher_id == "274" or publisher_id == "281":
            publisher_id = "6670"
        
        print(str(self.item_id) + " : " + self.release_name)

        return True


    def print_list(self):
        list_form = {"auth_token": "lwa-|" + config.AUTH_TOKEN }
        response = self.session.post(config.API_LIST_URL, headers = config.API_HEADERS, data = list_form)

        list_proto = comix_pb2.IssueResponse2()
        list_proto.ParseFromString(response.content)

        if len(list_proto.issues.issues) == 0:
            print("Could not find any book associated with this account . . .")
            return
        
        ids = []
        for issue in list_proto.issues.issues:
            ids.append(issue.id)
        
        for issue in self.get_issue_infos(ids):
            print(issue[0] + " : " + issue[1])


    def download(self):
        cwd = os.getcwd()
        output_folder = os.path.join(cwd, "comix_out")
        Path(output_folder).mkdir(exist_ok=True)
        content_folder = os.path.join(output_folder, self.release_name)
        Path(content_folder).mkdir(exist_ok=True)

        i = 0
        for page in self.comic.book.pages:
            print("\rDownloading page {0} . . .".format(str(i).zfill(3)), end='')
            for image in page.pageinfo.images:
                if image.type != image.Type.FULL:
                    continue
                image_key = comix_key.calculate_key(image.digest.data, self.item_id, self.comic.version, self.publisher_id, i)
                
                response = self.session.get(image.uri)
                with pyzipper.AESZipFile(io.BytesIO(response.content)) as zf:
                    zf.extractall(content_folder, pwd=image_key)
            i += 1

        i = 0
        for file in Path(content_folder).rglob("*"):
            extension = os.path.splitext(file)[1]
            if extension == ".jpg" or extension == ".png":
                os.rename(file, os.path.join(content_folder, "{0} - p{1}{2}".format(self.release_name, str(i).zfill(3), extension)))
            i += 1
        
        print("\nDone! Content saved to " + str(content_folder))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage:\ncomix <item_id>\n - Downloads the content for the specified item id\ncomix list\n - Lists all content associated with the current account")
        exit()
    
    if sys.argv[1] == "list":
        cmx = Cmx(None)
        cmx.print_list()
    else:
        cmx = Cmx(sys.argv[1])
        if cmx.get_comic():
            cmx.download()
