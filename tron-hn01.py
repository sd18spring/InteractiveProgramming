

import pygame
from pygame.locals import *
import time

pygame.init()
fpsClock = pygame.time.Clock()

WindowSurfaceObj = pygame.display.setmode((640,480))


class Cell(object):

    def __init__(self, height, x, y, flip = False):
        self.height = height
        self.x = x
        self.y = y
        self.flip = flip


    def __str__(self):
        return "Cell height=%f, x=%f, y=%f" % (self.height, self.x, self.y)




class Grid(object):
    """Defines a grid of cell objects"""
