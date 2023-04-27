from backend.FileIO.FileReadWrite import FileReadWrite
from backend.Intella.IntellaGeneric import IntellaGeneric
from backend.Translation.Translation import translate
from backend.OpenAI.OpenAI import OpenAI, Prompt
from twilio.rest import Client
import datetime
intella_obj = IntellaGeneric()
file_read_write_obj = FileReadWrite()


async def get_arabic_transcribe(session):
    try:
        path = file_read_write_obj.create_wav()
        intella_obj.post_audio(call_sid=session, filepath=path)
        arabic_transcribe = intella_obj.get_transcribe()
        if arabic_transcribe == "null":
            return 'not getting what you are looking for'
        return arabic_transcribe
    except Exception as e:
        print("get_openai_arabic_res", e)
        return 'not getting what you are looking for'


async def get_openai_arabic_res(session, eng_text):
    try:
        openai = OpenAI.factory(session)
        openai_resp = openai.get_response(Prompt("user", eng_text))
        print('OPEAN AI ENGLISH REPONSE:', openai_resp)
        return openai_resp
    except Exception as e:
        print("get_openai_arabic_res", e)
        return 'not getting what you are looking for'


def say_text_to_caller(account_sid, auth_token, ai_voice_response_mp3, callsid):
    client = Client(account_sid, auth_token)
    print('LAST Time in:', datetime.datetime.now())
    print('callsid, openai_resp_arb_mp3',callsid, ai_voice_response_mp3)
    string = str(ai_voice_response_mp3)
    print(string)
    client.calls(callsid).update(twiml=f'<Response><Play>{string}</Play><Connect><Stream name="Reconnect_Stream" url="wss://142f-43-228-231-218.ngrok-free.app/voice/stream/" /></Connect></Response>')
