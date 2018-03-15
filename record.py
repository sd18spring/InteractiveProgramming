import pyaudio
from pyaudio import *
import wave


def record(record_time, a_format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024):
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

    waveFile = wave.open('file.wav', 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(a_format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()





record(1)
