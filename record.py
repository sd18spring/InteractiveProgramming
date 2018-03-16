"""Running this in a separate file was necessary because that is the only way
to keep it from interrupting the game. While the main file was recording, it
would record every frame, which obviously caused problems. In order to communicate
with main, it writes to two files. file.wav is the data that record is getting,
stop.txt tells record when to stop.
"""
import pyaudio
from pyaudio import *
import wave
import os
from os.path import exists
import sys
import pickle
from pickle import dump, load


def record(record_time, a_format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024, file_name='file.wav'):
    """Records for a given amount of time, and stores the recording in file.wav
    by default. Don't change that, though, because classes reads file.wav.
    """
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



#First, stop.txt has to say something other that stop. Otherwise, record stops
#immediately.
f = open('stop.txt', 'wb')
insert = pickle.dumps('go')
f.write(insert)
f.close()

while True:
    #Then it repeatedly checks to see if stop.txt says stop, and if not, it records
    f = open('stop.txt', 'rb+')
    curr = f.read()
    f.seek(0, 0)
    update = pickle.loads(curr)

    if update=='stop':
        break

    record(0.2)
