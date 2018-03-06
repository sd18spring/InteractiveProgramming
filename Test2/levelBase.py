import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

class Level:
    """ The Base Class for Levels"""
    def getLayout(self):
        """Get the layout of the level
        Returns a list"""
        pass

    def getImages(self):
        """Get a list of all the images used by the level.
        Returnas a list of all the images used. The indices in the layout refer to sprites in the list returned by this function"""
        pass
