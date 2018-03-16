"""A collection of all of the classes and methods used to run the game, main
imports from here. Initially this was because we thought recording was going to
work differently than it had to. The way things ended up, main looks kind of silly.
"""
import pygame, sys, random
from pygame.locals import *

import pyaudio
from pyaudio import *
import wave
import time

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from numpy import arange

import pickle
from pickle import dump, load

SCREENWIDTH = 1500
SCREENHEIGHT = 1000

class Block(pygame.sprite.Sprite):
    """These are the obstacles that move towards you. They inherit from pygame's
    sprite class.
    """
    def __init__(self, screen, color, width, height):
        """Gives a size, color, and speed.
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.speedx = 10

    def update(self):
        """Moves the block according to its speed.
        """
        self.rect.left -= self.speedx
        if self.rect.right < 0:
            x_displacement = random.randint(0, SCREENWIDTH*2)
            self.rect.x = (SCREENWIDTH + x_displacement)
            self.rect.y = random.randrange(SCREENHEIGHT - 150)


class Player(pygame.sprite.Sprite):
    """This is also a sprite, but it is the block you control.
    """
    def __init__(self, screen, color, size, increment):
        """Gives the player a color, size, and sets how quickly it moves. Also
        initializes expected frequencies.
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.size = size
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.increment = increment
        self.is_recording = False

        #Initially, we wanted to calibrate the game to the user. This could be
        #implemented somewhat easily, but as it is, we ran out of time. Also,
        #we found these values worked for most people.
        self.calibrated_high = 100
        self.calibrated_low = 450

    def collide(self, obstacles, game):
        """Checks to see if the player has hit an obstacle.
        """
        if pygame.sprite.spritecollide(self, obstacles, False):
            #First, collide edits stop.txt to tell record to stop recording.
            f = open('stop.txt', 'wb')
            insert = pickle.dumps('stop')
            f.write(insert)
            f.close()

            #Then, it displays the score for a few seconds
            pygame.font.init()
            myfont = pygame.font.SysFont('Comic Sans MS', 300)
            textsurface = myfont.render("Score=%d"%(int(game.score)), False, (255, 255, 255))
            game.mainSurface.blit(textsurface,(275,400))
            pygame.display.update()
            time.sleep(2)

            #Then it quits.
            pygame.quit()
            sys.exit()

    def analyze_freq(self):
        """Analyze frequency uses a fast Fourier transform to get the frequency
        of file.wav, which is consistently being updated by record. It returns
        the frequency in Hz. FFT is somewhat imprecise with such short increments,
        and gets better the longer we record for, but also the game feels laggy.
        0.2 seconds is somewhat of a balance.
        """
        #A try clause was necessary, because occasionally, it will try to read
        #file.wav while record is trying to write to it, resulting in an error.
        #Our except clause keeps the previous values stored in fie.wav
        try:
            fs, data = wavfile.read('file.wav')
        except:
            data = self.data
            fs = self.fs

        self.data = data
        self.fs = fs

        a = data.T[0]
        b=[(ele/2**8.)*2-1 for ele in a]
        c = fft(b)

        d = len(c)//2

        k = arange(len(data))
        T = len(data)/fs
        frqLabel = k/T

        #Eccentricities in this algorithm make low frequencies appear very strongly,
        #So we look after the first few entries in the frequency list to get a more
        #accurate idea of what's going on.
        val = max(abs(c[2:(d-1)]))
        i = list(abs(c[2:(d-1)])).index(val)
        return frqLabel[2:(d-1)][i]

    def freq_movement(self, frequency):
        """Moves the player based on the detected frequency.
        """

        #First sets the middle frequency based on the high and low established in
        #init
        mid_freq = (self.calibrated_low + self.calibrated_high)/2
        if frequency < 70:
            pass

        elif frequency > mid_freq:
            #Then moves the correct direction, assuming that moving would not
            #move the player offscreen.
            if self.rect.y < self.increment:
                self.rect.y = 0
            elif self.rect.y > 0:
                self.rect.y -= self.increment

        elif frequency < mid_freq:
            if self.rect.y > SCREENHEIGHT-(self.size + self.increment):
                self.rect.y = SCREENHEIGHT - self.size
            elif self.rect.y < SCREENHEIGHT- self.size:
                self.rect.y += self.increment





class Game:
    """This class organizes the player and several obstacles, then runs and renders
    the game.
    """
    def __init__(self, num_blocks, player_color=(255, 0, 0)):
        """Makes a given number of obstacle blocks, then a player. Also prepares
        necessary pygame assets.
        """
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

        self.player = Player(self.mainSurface, player_color, 50, 10)
        self.player.rect.x = 200
        self.player.rect.y = 0.5*SCREENHEIGHT
        #The player has to be added to a group all by itself in order to be
        #drawn later.
        self.player_group.add(self.player)
        #Ha, comic sans was in the example we got, it doesn't actually do comic
        #sans, it just does some default font. This is fine.
        self.myfont = pygame.font.SysFont('Comic Sans MS', 150)

    def run(self):
        """Checks for the quit event, then moves everything as much as it needs
        to be moved and checkes for a collision, then draws everything. Then
        updates the score.
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    print(self.score)
                    pygame.quit()
                    sys.exit()

            freq = self.player.analyze_freq()
            self.player.freq_movement(freq)
            self.player.collide(self.blocksGroup, self)

            self.mainSurface.fill((0, 0, 0))
            textsurface = self.myfont.render(str(int(self.score)), False, (255, 255, 255))
            print(textsurface)
            self.player_group.draw(self.mainSurface)
            self.blocksGroup.update()
            self.blocksGroup.draw(self.mainSurface)
            self.mainSurface.blit(textsurface,(10,10))
            pygame.display.update()
            self.score += .1
