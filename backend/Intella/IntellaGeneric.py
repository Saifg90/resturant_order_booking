import requests
import os
import time
import datetime


class IntellaGeneric:
    def __init__(self):
        self.headers = {"Api-Token": os.environ["INTELLA_API_TOKEN_ID"]}
        self.url = f"https://api.intella-voice.com/api/accounts/{os.environ['INTELLA_API_ACCOUNT_ID']}/requests"
        self.payload = {}
        self.t_id = None

    def post_audio(self, call_sid=None, filepath=None):
        datetime.datetime.now()
        self.payload["fileName"] = call_sid
        self.payload['noOfSpeakers'] = 1
        file_send = [("file", (os.path.basename(str(filepath)), open(str(filepath), "rb"), "audio/wav"))]
        response = requests.post(self.url, headers=self.headers, data=self.payload, files=file_send)
        json_response = response.json()
        time.sleep(10)
        self.t_id = str(json_response["id"])

    def get_transcribe(self):
        payload = {}
        get_url = f"{self.url}/{self.t_id}"
        # get_url = self.url + "/" +'defe84e2-0a77-4dc6-84df-a4356642a
        response = requests.get(get_url, headers=self.headers, data=payload)
        json_get_response = response.json()
        return json_get_response["transcriptContent"]
