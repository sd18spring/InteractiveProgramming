import pygame
from pygame.locals import *
import time
from turtle import *

class PyGameWindowView(object):

    def __init__(self, size):

        self.screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    pygame.init()

    size = (640,480)
    turtle = Turtle()

    running = True
    while running:
        view = PyGameWindowView(size)
        position = pygame.mouse.get_pos()
        turtle.goto(position)
        time.sleep(.1)
    pygame.quit()


