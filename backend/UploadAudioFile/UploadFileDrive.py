import os
import dropbox

access_token = os.environ["DROPBOX_TOKEN"]
dbx = dropbox.Dropbox(access_token)

class UploadFile:
    def upload(self, filepath):
        dropbox_path = "/" + filepath.split("/")[-1]

        with open(filepath, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path)

        link = dbx.sharing_create_shared_link(dropbox_path).url
        
        direct_link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")

        return direct_link