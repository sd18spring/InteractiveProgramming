# -*- coding: utf-8 -*-
"""
@author: Grace Montagnino & Quinn Kelley
"""

import pygame
import random

from pygame.locals import *
import time

FPS = 50

class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.screenheight = pygame.display.get_surface().get_height()
        # self.screenwidth = pygame.display.get_surface().get_width()
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
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 255, 255),
                        pygame.Rect(self.model.puck.x,
                                    self.model.puck.y,
                                    self.model.puck.height,
                                    self.model.puck.width,
                                    ))
        pygame.display.update()

class Model(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.paddle = Paddle(50,10,0,240)
        self.paddle2=Paddle(50,10,630,240)
        self.puck=Puck(10,10,10,10)
    def update(self):
        """ Update the game state (currently only tracking the paddle) """
        self.paddle.update()
        self.paddle2.update()
        if int(self.puck.x)==int(self.paddle.x)+10 and (int(self.paddle.y)-50)<=int(self.puck.y)<=(int(self.paddle.y)+50):
            self.puck.vx=-self.puck.vx
            self.puckvy=-self.puck.vy
        if int(self.puck.x)==int(self.paddle2.x)-10 and (int(self.paddle2.y)-50)<=int(self.puck.y)<=(int(self.paddle2.y)+50):
            self.puck.vx=-self.puck.vx
            self.puck.vy=-self.puck.vy
        self.puck.update()

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
        self.vx = 0
        self.vy = 0

    def update(self):
        """ update the state of the paddle & stops it from running off the screen"""
        self.x += self.vx
        self.y += self.vy
        if self.y > 480 - self.height:
            self.y = 480 - self.height
        if 0 > self.y:
            self.y = 0
    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                        self.width,
                                                           self.x,
                                                          self.y)

class Puck(object):
    """ Encodes the state of the paddle in the game """
    def __init__(self,x,y,height,width):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height=height
        self.x,self.y=320,240
        self.width=width
        self.vx=1
        self.vy=0
        self.score1=0
        self.score2=0
        #to make starting v random do someting about making vx and vy random
        #self.vx=random.choice([-.6,-.4,-.2,.2,.4,.6])
        #self.vy=random.choice([-.6,-.4,-.2,.2,.4,.6])
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
    def update(self):
        """ update the state of the puck """
        if self.y>=480 or self.y<=0:
            self.vy=-self.vy
        if self.x>640:
            self.__init__(self.x,self.y,self.height,self.width)
            self.score2=self.score2+1
            font = pygame.font.Font(None, 36)
            Score2=int(self.score2)
            pygame.display.set_caption("Score:"+str(Score2))
        if self.x<=0:
            self.__init__(self.x,self.y,self.height,self.width)
            self.score1=self.score1+1
            font = pygame.font.Font(None, 36)
            Score1=int(self.score1)
            pygame.display.set_caption("Score:"+str(Score1))
        self.x += self.vx
        self.y+=self.vy
    def draw(self, surface):
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(pygame.Color(0,0,0))
        pygame.draw.rect(screen, (55,150,55), self.rect)
        self.x = self.rect.left
        self.y = self.rect.top
    def __str__(self):
        return "Puck x coordinate=%f, y coordinate=%f, radius=%f, width=%f" % (self.x,
                                                        self.y,
                                                           self.height,
                                                          self.w)

class PyGameKeyboardController(object):
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ arrow keys + WS modify the y position of the paddles"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
             self.model.paddle2.vy = -1
        elif pressed[pygame.K_DOWN]:
             self.model.paddle2.vy = 1
        else:
            self.model.paddle2.vy = 0
        if pressed[pygame.K_w]:
             self.model.paddle.vy = -1
        elif pressed[pygame.K_s]:
             self.model.paddle.vy = 1
        else:
            self.model.paddle.vy = 0

if __name__ == '__main__':
    pygame.init()

    size = (640, 480)

    model = Model(size)
    print(model)
    view = PyGameWindowView(model, size)
    controller = PyGameKeyboardController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        controller.handle_event(event)
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 0))
        model.update()
        view.draw()
        time.sleep(.001)
time.sleep(.001)

pygame.quit()
