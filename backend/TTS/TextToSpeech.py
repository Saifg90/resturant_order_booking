import time
import requests
import json
import os

class TextToSpeech:
    def __init__(self):
        self.headers = {
            'Authorization': os.getenv('TTS_API_KEY'),
            'X-User-ID': os.getenv('TTS_USER_ID'),
            'Content-Type': 'application/json'
        }

    async def request_audio_conversion(self, text):
        print('Requesting audio conversion', text)
        url = "https://play.ht/api/v1/convert"

        payload = json.dumps({
            "voice": "ar-SY-AmanyNeural",
            "content": [text],
        })

        response = requests.post(url, headers=self.headers, data=payload)
        print('TTS RESPONSE PLAY.HT',response.text)

        data = json.loads(response.text)
        time.sleep(5)
        return data


    async def get_audio(self, data):
        try: 
            url = f"https://play.ht/api/v1/articleStatus/?transcriptionId={data['transcriptionId']}"
            response = requests.get(url, headers=self.headers)
            audio = response.json()
            r = requests.get(audio['audioUrl'], allow_redirects=True)
            return r 
        except Exception as e:
            print(e)
        
       
