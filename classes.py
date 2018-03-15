import pygame, sys, random
from pygame.locals import *

import pyaudio
from pyaudio import *
import wave

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from numpy import arange

SCREENWIDTH = 1500
SCREENHEIGHT = 1000
WAVE_OUTPUT_FILENAME = "file.wav"

class Block(pygame.sprite.Sprite):
    def __init__(self, screen, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.speedx = 10

    def update(self):
        self.rect.left -= self.speedx
        if self.rect.right < 0:
            x_displacement = random.randint(0, SCREENWIDTH*2)
            self.rect.x = (SCREENWIDTH + x_displacement)
            self.rect.y = random.randrange(SCREENHEIGHT - 150)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, color, size, increment):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.size = size
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.increment = increment
        self.is_recording = False

        self.calibrated_high = 100
        self.calibrated_low = 450

    def on_event(self, event):

        if event.type == KEYDOWN:

            if self.rect.y > SCREENHEIGHT-(self.size + self.increment):
                self.rect.y = SCREENHEIGHT - self.size
            elif self.rect.y < SCREENHEIGHT- self.size:
                self.rect.y += self.increment



        elif event.type == MOUSEBUTTONDOWN:
            if self.rect.y < self.increment:
                self.rect.y = 0
            elif self.rect.y > 0:
                self.rect.y -= self.increment

    def collide(self, obstacles, score):
        if pygame.sprite.spritecollide(self, obstacles, False):
            print(int(score))
            pygame.quit()
            sys.exit()

    def record(self, record_time, a_format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024):
        self.is_recording = True
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

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audio.get_sample_size(a_format))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        self.is_recording = False


    def analyze_freq(self, filename='file.wav'):
        fs, data = wavfile.read(filename) # load the data
        a = data.T[0] # this is a two channel soundtrack, I get the first track
        b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
        c = fft(b) # calculate fourier transform (complex numbers list)

        #print(abs(max(c)))
        d = len(c)//2  # you only need half of the fft list (real signal symmetry)

        k = arange(len(data))
        T = len(data)/fs  # where fs is the sampling frequency
        frqLabel = k/T

        val = max(abs(c[2:(d-1)]))
        i = list(abs(c[2:(d-1)])).index(val)
        return frqLabel[2:(d-1)][i]

    def remap_interval(self, val,
                       input_interval_start,
                       input_interval_end,
                       output_interval_start=0,
                       output_interval_end=SCREENHEIGHT):
        input_interval = input_interval_end - input_interval_start
        output_interval = output_interval_end - output_interval_start
        val_interval = val - input_interval_start

        scale_factor = output_interval/input_interval
        new_val = output_interval_start+(scale_factor*val_interval)
        return new_val

    def freq_movement(self, frequency):
        frequencyish = self.remap_interval(frequency, self.calibrated_high, self.calibrated_low)
        if frequencyish > self.rect.y:
            self.rect.y -=20
        elif frequencyish < 50:
            pass
        elif frequencyish < self.rect.y:
            self.rect.y += 20





class Game:
    def __init__(self, num_blocks, player_color=(255, 0, 0)):
        pygame.init()

        self.mainSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
        pygame.display.set_caption("Collision Game")
        self.blocksGroup = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.score = 0

        for i in range(num_blocks):
            height = random.randint(30, 150)
            weight = random.randint(30, 150)
            myBlock = Block(self.mainSurface, (255, 255, 255), weight, height)
            x_displacement = random.randint(0, SCREENWIDTH)
            myBlock.rect.x = (SCREENWIDTH + x_displacement)
            myBlock.rect.y = random.randrange(SCREENHEIGHT - 150)
            self.blocksGroup.add(myBlock)

        self.player = Player(self.mainSurface, player_color, 50, 20)
        self.player.rect.x = 200
        self.player.rect.y = 0.5*SCREENHEIGHT
        self.player_group.add(self.player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    print(self.score)
                    pygame.quit()
                    sys.exit()
                self.player.on_event(event)
            # if self.player.is_recording == False:
            #     self.player.record(0.2)
            freq = self.player.analyze_freq()
            self.player.freq_movement(freq)
            self.mainSurface.fill((0, 0, 0))

            self.player.collide(self.blocksGroup, self.score)

            self.player_group.draw(self.mainSurface)
            self.blocksGroup.update()
            self.blocksGroup.draw(self.mainSurface)
            pygame.display.update()
            self.score += .01
