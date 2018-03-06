# -*- coding: utf-8 -*-
"""
This is a worked example of applying the Model-View-Controller (MVC)
design pattern to the creation of a simple arcade game (in this case
Brick Breaker).

We will create our game in stages so that you can see the process by
which the MVC pattern can be utilized to create clean, extensible,
and modular code.

@author: SoftDesProfs
"""

import pygame
from pygame.locals import *
import time

class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))

        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         pygame.Rect(self.model.paddle.x,
                                     self.model.paddle.y,
                                     self.model.paddle.width,
                                     self.model.paddle.height))
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 255, 255),
                         pygame.Rect(self.model.paddle2.x,
                                     self.model.paddle2.y,
                                     self.model.paddle2.width,
                                     self.model.paddle2.height))
        pygame.display.update()

class Model(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.paddle = Paddle(50,10,0,240)
        self.paddle2=Paddle(50,10,630,240)
    def update(self):
        """ Update the game state (currently only tracking the paddle) """
        self.paddle.update()
        self.paddle.update()
    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        output_lines.append(str(self.paddle))
        # print one item per line
        return "\n".join(output_lines)
class Paddle(object):
    """ Encodes the state of the paddle in the game """
    def __init__(self, height, width, x, y):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0

    def update(self):
        """ update the state of the paddle """
        self.x += self.vx

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                        self.width,
                                                           self.x,
                                                          self.y)


if __name__ == '__main__':
    pygame.init()

    size = (640, 480)

    model = Model(size)
    print(model)
    view = PyGameWindowView(model, size)
    #controller = PyGameKeyboardController(model)
    #controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            #controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    #pygame.quit()
