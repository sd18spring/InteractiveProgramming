import pyaudio
from pyaudio import *
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"



# audio = pyaudio.PyAudio()
#
# # start Recording
# stream = audio.open(format=FORMAT, channels=CHANNELS,
#                 rate=RATE, input=True,
#                 frames_per_buffer=CHUNK)
# print("recording...")
# frames = []
#
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
# print("finished recording")
#
#
# # stop Recording
# stream.stop_stream()
# stream.close()
# audio.terminate()
#
# waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(frames))
# waveFile.close()

def record(record_time, a_format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(rate / chunk * record_time)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(a_format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

record(1)
