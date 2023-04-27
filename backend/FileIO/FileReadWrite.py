import os
import io
import wave
import numpy as np
import datetime
from backend.UploadAudioFile.UploadFileDrive import UploadFile
import time
class FileReadWrite:
    def __init__(self):
        self.files_path = os.path.join(
            os.getcwd(), "backend", "FileIO", "Files")
        self.txt_file = os.path.join(self.files_path, "audio_bytes_data.txt")
        self.wav_file = os.path.join(self.files_path, "customer_audio.wav")
        self.total_s = 15 * 50  # 15 seconds audio 1 sec = 50 frames
        self.openai_resp = None
        self.sil_count = 0
        self.ai_mp3_file = None

    def write_audio(self, data=None):
        lines = f"{data}\n"
        self.verify_silence(data)
        with open(self.txt_file, "a") as byte_file:
            byte_file.write(lines)
        self.total_s -= 1

    def ms_count_verify(self):
        if self.total_s == 0:
            return 'Written'
        elif self.sil_count == 500:
            print('It is Silience since 10 sec')
            self.sil_count = 0
            return 'Silence'

    def create_wav(self):
        with wave.open(self.wav_file, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            with open(self.txt_file, "r") as data_file:
                buf = io.StringIO(data_file.read())
                for line in buf:
                    byte_data = bytes(eval(line))
                    f.writeframes(byte_data)

        return self.wav_file

    def reset_files(self):
        self.total_s = 15 * 50  # reset count
        # to clear text file for next iteration
        open(self.txt_file, "w").close()
        os.remove(self.wav_file)
        os.remove(self.ai_mp3_file)

    def verify_silence(self, audio_data):
        numpy_array = np.frombuffer(audio_data, dtype=np.int16)
        rms = np.sqrt(np.mean(np.abs(numpy_array ** 2)))
        silence_threshold = 100
        if rms < silence_threshold:
            self.sil_count += 1
            # print("Audio contains silence")
        else:
            self.sil_count = 0
            # print("Audio does not contain silence")

    def create_ai_mp3(self, r):
        self.ai_mp3_file = os.path.join(
            self.files_path, f"{datetime.datetime.now().timestamp()}_AI_VOICE_RESPONSE.mp3")
        try: 
            open(self.ai_mp3_file, 'wb').write(r.content)
            upload_file = UploadFile()
            uploaded_link = upload_file.upload(self.ai_mp3_file)
            time.sleep(10)
            return uploaded_link
        except Exception as e:
            print(e)
            return "error"

