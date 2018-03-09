import pygame
from pygame.locals import *
from pygame.font import *
import time
import numpy

pygame.init()


class Model(object):
    """keeps track of the game state"""
    def __init__(self, environmentobjs, road, player):
        #initialize array that road will cycle through
        self.arena_array = numpy.zeros(3,3,3)
        #environment objects will be tethered to a position on the road below
        self.road = road
        self.player = Player()

class EnvironmentObjects(object):
    """base class for objects"""
    def __init__(self):
        pass

class Gastanks(EnvironmentObjects):
    """describing type of EnvironmentObject"""
    pass

class Pedestrians(EnvironmentObjects):
    """describing type of EnvironmentObject"""
    pass

class Obstacles(EnvironmentObjects):
    """describing type of EnvironmentObject"""
    pass

class Road():
    """describing the surface that will bring objects to the player"""
    def __init__(self, pedestrians, gastanks, obstacles):
        self.pedestrians = Pedestrians
        self.gastanks = Gastanks
        self.obstacles = Obstacles

class Player():
    """user controlled player"""
    def __init__(self, position=(0,0)):
        self.position = position

class View():
    """drawing what is in the model"""
    def __init__(self, model):
        self.model = model

class Controllers():
    """keyboard controls"""
    def __init__(self, model):
        self.model = model
    #def __init__(self, )
    #def move_right
    #def move_left
    #def move_up


if __name__ == "__main__":
    size = (640, 480)
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        time.sleep(.001)

    pygame.quit()
