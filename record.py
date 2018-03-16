import pyaudio
from pyaudio import *
import wave
import os
from os.path import exists
import sys
import pickle
from pickle import dump, load


def record(record_time, a_format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024, file_name='file.wav'):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=a_format, channels=channels,
                    rate=rate, input=True,
                    frames_per_buffer=chunk)

    frames = []
    for i in range(0, int(rate / chunk * record_time)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(a_format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()



f = open('stop.txt', 'wb')
insert = pickle.dumps('go')
f.write(insert)
f.close()

while True:
    f = open('stop.txt', 'rb+')
    curr = f.read()
    #print("curr = ", curr)
    f.seek(0, 0)
    update = pickle.loads(curr)
    #print("update = ", update)

    if update=='stop':
        #print(update)
        break
    record(0.2)
