import dropbox



def upload_file_to_dropbox(local_file_path, access_token):
    dbx = dropbox.Dropbox(access_token)

    dropbox_path = "/" + local_file_path.split("/")[-1]

    # Upload the file to Dropbox
    with open(local_file_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path)

    # Create a Dropbox shared link to the uploaded file
    link = dbx.sharing_create_shared_link(dropbox_path).url

    # Convert the link to a direct download link
    direct_link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")

    return direct_link

print(upload_file_to_dropbox("/home/fx-data/Desktop/rest_ai_voice/backend/FileIO/Files/AI_VOICE_RESPONSE.mp3","sl.BcbySFYYbpQMgWJiyZ65PvfmImOez4aKLmAdOBvBoybD9mm26U8BDooU_I30S8LlfP7923iIu27my53fhBEwJmr1nHLrTCDkJ053s-nbp-ht6ACoba9N07TdqjiP7tH_nyAd1UMATDnQ"))