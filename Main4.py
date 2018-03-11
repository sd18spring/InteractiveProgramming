import pygame
import time
import random
import cv2
import numpy as np

class PyGameWindowView(object):
    """ Provides a view of the Dodgy Game model in a pygame
        window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.size = size
        self.screen = pygame.display.set_mode(size)


    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(255, 255, 255))
        self.bomb1 = pygame.transform.scale(
            pygame.image.load('bomb1.png'), (100, 100))
        self.bomb2 = pygame.transform.scale(
            pygame.image.load('bomb2.png'), (100, 100))
        self.screen.blit(self.bomb1, (self.model.bomb.center_x, self.model.bomb.center_y))
        pygame.display.update()

class Model(object):
    def __init__(self,size):
        self.width = size[0]
        self.height = size[1]
        self.bomb_init_height = -200
        self.bomb_moving_sped = 0.5
        self.bomb = Bomb(random.randrange(0,self.width), self.bomb_init_height, self.bomb_init_height, self.height, self.width, self.bomb_moving_sped)

    def update(self):
        self.bomb.update()


class Bomb(object):
    """ Represents a bird in dodging game """
    def __init__(self, center_x, center_y, start_y, display_width, display_height, moving_speed):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.start_y = start_y
        self.display_width = display_width
        self.display_height = display_height
        self.moving_speed = moving_speed

    def update(self):

        # update the position of bomb each time
        self.center_y += self.moving_speed
        # if the bomb achieve the bottom of the screen
        if self.center_y >self.display_height:
            self.center_y = self.start_y
            self.center_x = random.randrange(0, self.display_width)

class User(object):
    """ Represents the user in my dodging game """

    def __init__(self, center_x, center_y):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        # self.radius = radius

class Heart(object):
    '''represents the number of lives that the user has left. The player always starts with 3 lives'''

    def __init__(self, left, top , width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

if __name__ == '__main__':
    pygame.init()
    size = (800, 600)
    model = Model(size)
    view = PyGameWindowView(model, size)
    running = True
    while running:
        model.update()
        view.draw()
        time.sleep(.001)
    pygame.quit()