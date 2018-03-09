import pygame
pygame.init()
screen = pygame.display.set_mode([300,200])



class Model():
    def __init__(self, environment, road, player):
        self.environment = environment
        self.road = road
        self.play = player

class Environment():
    def __init__(self, road):
        self.road = road

class Road():
    def __init__(self, pedestrians = [], gastanks = []):
        self.pedestrians = pedestrians
        self.gastanks = gastanks

class Player(:)
    def __init__(self, position=(0,0)):
        self.position = position

#class UserInterface

class Controllers():
    #def __init__(self, )
    #def move_right
    #def move_left
    #def move_up
class View(Model):
    def __init__(self)
