import pygame, sys, random
from pygame.locals import *

import pyaudio
from pyaudio import *
import wave

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from numpy import arange


x = 0
try:
    fs, data = wavfile.read('figfeks.wav')
except:
    x = 3

print(x)
