import pygame
from pygame.locals import *
import time
from turtle import *
import os

class PyGameWindowView(object):

    def __init__(self, model, size):

        self.screen = pygame.display.set_mode(size)
        self.model = model

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))

        self.lineStart = (0, 240)
        self.drawColor = (0, 0, 0)
        self.lineWidth = 10

    def draw(self):

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
        #view.lineStart = pygame.mouse.get_pos()
        lineEnd = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pygame.draw.line(view.background, view.drawColor, view.lineStart, lineEnd, view.lineWidth)
            view.lineStart = lineEnd
        view.screen.blit(view.background, (0, 0))
        pygame.display.flip()
        #position = pygame.mouse.get_pos()

        view.draw()
        #print(lineEnd[0]-5, view.lineEnd[1]-5)
        model.update(lineEnd[0]-150, lineEnd[1]-20)
        print(model.x, model.y)
        pygame.display.update() #this is the line of code I added to update the screen
        time.sleep(.001)
    pygame.quit()
