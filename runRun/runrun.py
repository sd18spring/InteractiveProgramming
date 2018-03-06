import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


class RunRunMain:

    def __init__(self, width=640, height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))


    def MainLoop(self):
        """This is the Main Loop of the Game"""

        """Load All of our Sprites"""
        self.LoadSprites()

        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def LoadSprites(self):
        pass

class Player:
    pass


class Coin(pygame.sprite.Sprite):
    pass


class Ground(pygame.sprite.Sprite):
    pass


if __name__ == "__main__":
    MainWindow = RunRunMain()
    MainWindow.MainLoop()
