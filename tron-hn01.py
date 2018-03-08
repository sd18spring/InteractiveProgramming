

import pygame
from pygame.locals import *
import time

pygame.init()
fpsClock = pygame.time.Clock()

WindowSurfaceObj = pygame.display.setmode((640,480))

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
        for cell in self.model.cells:
            pygame.draw.cell(self.screen,
                             pygame.Color(cell.color),
                             pygame.Rect(brick.x,
                                         brick.y,
                                         brick.height))


        pygame.display.update()


class Cell(object):

    def __init__(self, height, x, y, flip = False):
        self.height = height
        self.x = x
        self.y = y
        self.flip = flip
        self.color = (0,0,0)


    def __str__(self):
        return "Cell height=%f, x=%f, y=%f" % (self.height, self.x, self.y)

    def __hit__(self, player):
        self.flip = True
        self.color = player.color




class Grid(object):
    """Defines a grid of cell objects"""
    def __init__(self, screen_height, screen_width):
        self.cells = []
        n=30
        dx = screen_width/ n
        stack_height = screen_height// dx
        for i in range(n):
            for j in range(stack_height):
                cell = Cell(dx,(i*dx),(j*dx))
                self.cells.append(cell)
