import pygame
from pygame.locals import *
import time

class SnakeGame(object):
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def mainloop(self):

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
class Mouse(object):

    def __init__(self, height, width, x, y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __str__(self):
        return 'Mouse is in %f, %f' % (self.x, self.y)

if __name__ == '__main__':
    window = SnakeGame(640, 800)
    window.mainloop()
