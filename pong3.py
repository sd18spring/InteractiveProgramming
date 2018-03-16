import pygame
from pygame.locals import *
import time
import os
import random
import math
import sys
import cv2
import numpy as np


class PyGameWindowView(object):
    """ A view of the Pong game rendered in a PyGame Window"""
    def __init__(self, model, size):
        """ Initialize the PyGame window of the game """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """Draw the current game state to the screen"""
        self.screen.fill(pygame.Color(135, 206, 250))
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 127, 80),
                        pygame.Rect(self.model.paddle1.x,
                                    self.model.paddle1.y,
                                    self.model.paddle1.width,
                                    self.model.paddle1.height))
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 127, 80),
                        pygame.Rect(self.model.paddle2.x,
                                    self.model.paddle2.y,
                                    self.model.paddle2.width,
                                    self.model.paddle2.height))

        pygame.draw.circle(self.screen,
                           pygame.Color(255,255,102),
                           (self.model.ball.x,
                           self.model.ball.y),
                           self.model.ball.radius)

        pygame.display.update()


class PongModel(object):
    """Encodes a model of the game state"""

    def __init__(self,size):
        self.width = size[0]
        self.height = size[1]
        self.paddle1 = Paddle(100, 20, 10, self.height)
        self.paddle2 = Paddle(100, 20, self.width - 30, self.height / 2)
        self.ball = Ball(int(self.width/2), int(self.height/2), int(10), 10)

    def update(self):
        """Left Paddle"""
        self.paddle1.update()
        """Right Paddle"""
        self.paddle2.update()


        """Movement of ball when it touches screen boundaries"""
        if self.ball.x < 500 or self.ball.x > 0:
            self.ball.x = self.ball.x + int(self.ball.vx)
        else:
            self.ball.x = self.ball.y - int(self.ball.vx)
        if self.ball.y < 500 or self.ball.y > 0:
            self.ball.y = self.ball.y + int(self.ball.vy)
        else:
            self.ball.y = self.ball.y  - int(self.ball.vy)

        """Movement of the ball when it touches paddles"""


        right = self.ball.x + self.ball.radius
        left = self.ball.x - self.ball.radius
        top = self.ball.y - self.ball.radius
        bottom = self.ball.y + self.ball.radius



        if right == self.paddle2.x and self.ball.y >= self.paddle2.y and self.ball.y <= self.paddle2.height + self.paddle2.y:
            self.ball.vx = self.ball.vx * -1

        if left == self.paddle1.x + self.paddle1.width and self.ball.y >= self.paddle1.y and self.ball.y <= self.paddle1.height + self.paddle1.y:
            self.ball.vx = self.ball.vx * -1



        """Boundaries for the ball and paddles"""
        if self.paddle1.y > 700:
            self.paddle1.y = 700
        if self.paddle1.y < 0:
            self.paddle1.y = 0
        if self.paddle2.y > 700:
            self.paddle2.y = 700
        if self.paddle2.y < 0:
            self.paddle2.y = 0
        if self.ball.y >= 800:
            self.ball.vy = -self.ball.vy
        if self.ball.y <= 0:
            self.ball.vy = -self.ball.vy
        if self.ball.x < self.paddle1.x:
            pygame.display.quit()
        if self.ball.x > self.paddle2.x:
            pygame.display.quit()
        # if self.ball.
    def __str__(self):
        output_lines = []

        output_lines.append(str(self.paddle1))
        output_lines.append(str(self.paddle2))
        output_lines.append(str(self.ball))

        return "\n".join(output_lines)

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, speed):

        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.vy = random.choice([-1,1])
        self.vx = random.choice([-1,1])


    # def update(self, ball, paddle1, paddle2, vx, vy):
    #
    #     if self.ball.x == -1 and self.ball.x == 10:
    #         return -1
    #     elif self.ball.x == 1 and self.paddle2.width == self.ball.x:
    #         return -1
    #     else:
    #         return 1
    #     self.x += self.vx
    #     self.y += self.vy

    def __str__(self):
        return "Ball x=%f, y=%f, radius=%f" % (self.x, self.y, self.radius)


class Paddle(pygame.sprite.Sprite):
    """Encodes the state of the paddle 1 in the game"""

    def __init__(self, height, width, x, y):
        """Initalize a paddle with the sepcified height, width, and position (x,y) """

        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = 0.0

    def update(self):
        """update the state of the paddle"""

        self.y += self.vy

    def update_position(self, coordinate):
        self.y = coordinate

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height, self.width, self.x, self.y)

class PyGameMouseController(object):

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.model.paddle1.y = event.pos[1] - self.model.paddle1.height/2.0


class PyGameKeyboardController(object):

    def __init__(self,event):
        self.model = model

    def handle_event(self,event):

        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.paddle2.vy += -2.0
        else:
            self.model.paddle2.vy = 0.0
        if event.key == pygame.K_DOWN:
            self.model.paddle2.vy += 2.0


if __name__ == '__main__':
    pygame.init()

    FPS = 200
    size = (1800, 800)
    model = PongModel(size)
    view = PyGameWindowView(model, size)

    controller1 = PyGameMouseController(model)
    controller2 = PyGameKeyboardController(model)

    fps_clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                 running = False
            controller1.handle_event(event)
            controller2.handle_event(event)
        # ball = pygame.draw.circle
        # # ball = Ball(int((size[0])/2), int(size[1]/2), int(10), 10)
        # # view.screen.blit(ball, (0, 0))

        model.update()
        view.draw()
        time.sleep(.001)
        fps_clock.tick(FPS)

    pygame.quit()
