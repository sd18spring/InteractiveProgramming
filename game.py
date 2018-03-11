import pygame
from pygame.locals import *
from pygame.font import *
import time
import numpy
import random
pygame.init()


class Model(object):
    """keeps track of the game state"""
    def __init__(self, road):
        #initialize array that road will cycle through
        self.arena_array = numpy.zeros((5,5,5), dtype=numpy.object_)
        #environment objects will be tethered to a position on the road below
        self.road = Road()
        self.player = Player(4,2)

    def __str__(self):
        return str(self.arena_array)

    def place_player(self):
        self.arena_array[0,self.player.x,self.player.y] = self.player

    def move_road(self):
        self.arena_array[:,:,4] = road.add_obj(4)
        road_pos = 4
        while True:
            self.arena_array[road_pos-1,:,:] = self.arena_array[road_pos,:,:]
            self.arena_array[road_pos,:,:] = numpy.zeros((5,5), dtype=numpy.object_)
            road_pos -= 1
            print(self.__str__())
            time.sleep(1)
            if road_pos==0:
                break

class EnvironmentObject():
    """base class for objects"""
    def __init__(self):
        pass


class Gastanks(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self):
        pass

class Pedestrians(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self):
        pass

class Obstacles(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init(self):
        pass

class Road():
    """describing the surface that will bring objects to the player"""
    def __init__(self):
        self.road_matrix = numpy.zeros((5,5),dtype=numpy.object_)

    def __str__(self):
        return str(self.road_matrix)

    def add_obj(self, x_pos):
        gas = Gastanks()
        ped = Pedestrians()
        obst = Obstacles()
        obj_list = [gas, ped, obst]
        obj = obj_list[random.randint(0,2)]
        self.road_matrix[4, x_pos] = obj
        return self.road_matrix

class Player():
    """user controlled player"""
    def __init__(self, x_pos, y_pos, gas_level = 100, start_score=0):
        self.x = x_pos
        self.y = y_pos
        self.gas_level = gas_level
        self.score = start_score
    def __str__(self):
        return '4'

class View():
    """drawing what is in the model"""
    def __init__(self, model):
        self.model = model

class Controllers():
    """keyboard controls"""
    def __init__(self, model):
        self.model = model
        self.player = Player()
    #def move_right
    #def move_left
    #def move_up

class Menu():
    """base class for main and pause menus"""
    pass

class MainMenu(Menu):
    """main menu"""
    pass

class PauseMenu(Menu):
    """pause menu"""
    pass

class Hud():
    """display current score and gas level"""
    def __init__(self):
        self.player = Player()

if __name__ == "__main__":
    road = Road()

    model = Model(road)
    model.place_player()
    print(model)
    model.move_road()










#MAIN GAME LOOP:
    #size = (640, 480)
    #screen = pygame.display.set_mode(size)
    #pygame.display.set_caption('ROAD RAGE')
    #running = True
    #while running:
        #for event in pygame.event.get():
            #if event.type == QUIT:
                #running = False
        #time.sleep(.001)

    #pygame.quit()


#testing
