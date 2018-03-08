import pygame
from pygame.locals import *
import time
from turtle import *
import os

class PyGameWindowView(object):

    def __init__(self, model, size):

        self.screen = pygame.display.set_mode(size)
        self.model = model
    def draw(self):
        self.screen.fill(pygame.Color(255, 255, 255))

        pygame.draw.rect(self.screen,
                         pygame.Color(0, 0, 0),
                         pygame.Rect(self.model.x,
                                     self.model.y,
                                     self.model.width,
                                     self.model.height))


class Paddle(object):
    """ Encodes the state of the paddle in the game """
    def __init__(self, size):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height = 20
        self.width = 100
        self.x = 200
        self.y = 30

    def update(self, positionx, positiony):
        """ update the state of the paddle """
        self.x = positionx
        self.y = positiony

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                            self.y)

if __name__ == '__main__':
    pygame.init()

    size = (640,480)

    model = Paddle(size)
    view = PyGameWindowView(model, size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        position = pygame.mouse.get_pos()
        view.draw()
        print(position[0], position[1])
        model.update(position[0], position[1])
        print(model.x, model.y)
        pygame.display.update() #this is the line of code I added to update the screen
        time.sleep(.001)
    pygame.quit()
