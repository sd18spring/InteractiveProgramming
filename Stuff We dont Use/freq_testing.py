import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from numpy import arange

import pyaudio
from pyaudio import *
import wave

from sound_experimentation import record
from freq_test import analyze


while True:
    record(0.2)
    analyze()
