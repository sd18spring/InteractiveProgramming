import pygame, sys
from pygame.locals import *
from pygame.font import *
import time
import numpy
import random
pygame.init()


class Model(object):
    """keeps track of the game state"""
    def __init__(self):

        self.player = Player(295, 200)

    def update(self):
        self.player.update()



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

#class Road():
#    """describing the surface that will bring objects to the player"""
#    def __init__(self):
#        self.road_matrix = numpy.zeros((5,5),dtype=numpy.object_)
#
#    def __str__(self):
#        return str(self.road_matrix)
#
#    def add_obj(self, x_pos):
#        gas = Gastanks()
#        ped = Pedestrians()
#        obst = Obstacles()
#        obj_list = [gas, ped, obst]
#        obj = obj_list[random.randint(0,2)]
#        self.road_matrix[4, x_pos] = obj
#        return self.road_matrix

class Player():
    """user controlled player"""
    def __init__(self, x_pos, y_pos, gas_level = 100, start_score=0):
        self.x = x_pos
        self.y = y_pos
        self.gas_level = gas_level
        self.score = start_score
        self.rect = pygame.Rect(self.x, self.y, 50, 80)
        self.image = pygame.image.load('car.jpg')
        self.image = pygame.transform.scale(self.image, (50,80))
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        if self.x > 640 or self.x < 0:
            self.vx = 0
            self.x += self.vx
        else:
            self.x += self.vx

        if self.y > 480 or self.y < 0:
            self.vy = 0
            self.y += self.vy
        else:
            self.y += self.vy


    def __str__(self):
        return '4'

class View():
    """drawing what is in the model"""
    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((640,480))

    def draw(self):
        """Draw the current game state on the screen"""
        self.screen.fill(pygame.Color(0,0,0))
        width = 50
        height = 80
        #self.screen.blit(self.model.player.image, self.model.player.rect)
        pygame.draw.rect(self.screen,
                         pygame.Color(255,255,255),
                         pygame.Rect(self.model.player.x,
                                     self.model.player.y, 50, 80))

#pygame.Rect(player.x,
#player.y,
#width,
#height))
        pygame.display.update()

class Controllers(object):
    """keyboard controls"""
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        pygame.key.set_repeat(1,50)
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.player.y -= 10
        if event.key == pygame.K_DOWN:
            self.model.player.y += 10
        if event.key == pygame.K_LEFT:
            self.model.player.x -= 10
        if event.key == pygame.K_RIGHT:
            self.model.player.x += 10
        


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
FPS = 30
fpsClock = pygame.time.Clock()




if __name__ == "__main__":
    #player = Player(295, 200)

    pygame.init()
    model = Model()
    #screen = pygame.display.set_mode((640,480))
    view = View(model)
    controller = Controllers(model)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)
    pygame.quit()








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




#if direction == 'right':
#    carx += 5
#
#    if carx == 350:
#        direction == 'down'
#elif direction == 'down':
#    cary += 5
#    if cary == 480:
#        direction == 'left'
#if direction == 'left':
#    carx += 5

#    if carx == 20:
#        direction == 'up'
#elif direction == 'up':
#    cary += 5
#    if cary == 10:
#        direction == 'right'
