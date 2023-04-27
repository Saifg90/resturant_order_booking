from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from channels.generic.websocket import AsyncJsonWebsocketConsumer

import os
import json
import base64
from audioop import ulaw2lin, ratecv
import datetime
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Connect

from backend.FileIO.FileReadWrite import FileReadWrite
from backend.Intella.IntellaGeneric import IntellaGeneric
from backend.TTS.TextToSpeech import TextToSpeech
from backend.Translation.Translation import translate
from backend.dbservice.redis import RedisStorage
from backend.Twillo.Twillo import Twillo
from voice.utils import get_arabic_transcribe, get_openai_arabic_res, say_text_to_caller


file_read_write_obj = FileReadWrite()
intella_obj = IntellaGeneric()
redis = RedisStorage().factory()
twl_obj = Twillo()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_client = Client(account_sid, auth_token)


@csrf_exempt
def call(request):
    """Accept a phone call."""
    voice_response_obj = VoiceResponse()
    voice_response_obj.say("طيب، شو نوع الوجبة اللي بدك اياها؟ وشو نوع السلطة بدك اياها؟",language='ar')
    connect = Connect()
    connect.stream(url=f"wss://{request.get_host()}/voice/stream/")
    Caller = request.GET.get("From")
    redis.set_key('Caller', str(Caller[1:]))
    CallSid = request.GET.get("CallSid")
    redis.set_key('CallSid', CallSid)
    voice_response_obj.append(connect)
    voice_response_obj.pause(30)
    return HttpResponse(str(voice_response_obj), content_type="text/xml")

class StreamConsumer(AsyncJsonWebsocketConsumer):
    """Receive and arabic_transcribe audio stream."""

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        session = redis.get_key('Caller')[0]
        callsid = redis.get_key_callsid('CallSid')
        packet = json.loads(text_data)

        if packet["event"] == "Connect":
            print("Streaming is Connecting")

        elif packet["event"] == "stop":
            print("\nStreaming has stopped")

        elif packet["event"] == "media":

            audio_data = base64.b64decode(packet["media"]["payload"])
            audio_data = ulaw2lin(audio_data, 2)
            audio_data = ratecv(audio_data, 2, 1, 8000, 16000, None)[0]

            file_read_write_obj.write_audio(audio_data)

            if file_read_write_obj.ms_count_verify() == 'Written':
                print("file is written")
                arabic_transcribe = await get_arabic_transcribe(session)
                print("intela output", arabic_transcribe)

                openai_resp_arb = await get_openai_arabic_res(session, arabic_transcribe)
                print("openAI response", openai_resp_arb)

                tts_mp3 = TextToSpeech()
                data = await tts_mp3.request_audio_conversion(openai_resp_arb)
                print("tts transcript id", data)

                ai_voice_response_mp3_r = await tts_mp3.get_audio(data)
                print(ai_voice_response_mp3_r, "tts audio res")

                ai_voice_response_mp3 = file_read_write_obj.create_ai_mp3(ai_voice_response_mp3_r)
                print(ai_voice_response_mp3, "tts audio conversion")
                
                client = Client(account_sid, auth_token)
                print('LAST Time:',datetime.datetime.now())
                say_text_to_caller(account_sid, auth_token, ai_voice_response_mp3, callsid)
                # file_read_write_obj.reset_files()
            elif file_read_write_obj.ms_count_verify() == 'Silence':
                say_text_to_caller(account_sid, auth_token, 'Can you repeat your order Please?', callsid)
                # file_read_write_obj.reset_files()

    async def disconnect(self, *args, **kwargs):
        session = redis.get_key('Caller')[0]
        redis.remove_key(session)
        print("disconnected")
        
class TwillioOutgoing(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client = Client(account_sid, auth_token)
        twiml = f"""<Response>
                    <Play>https://dl.dropboxusercontent.com/s/3eug6f6pr14di53/1681451724.450368_AI_VOICE_RESPONSE.mp3</Play>
                </Response>"""
        call = client.calls.create(
            twiml=twiml, to="+919999999999", from_="+15075708442"
        )
        return Response(str(call.sid), content_type="text/xml")