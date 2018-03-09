#THIS FILE IS DOPE
import pygame
from pygame.locals import *
import time


class Penguin(pygame.sprite.Sprite): # code is from pygame documenta
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super.__init__()

        # Create an image of the block, and fill it with a color
        self.image = pygame.image.load("penguin_smol.png").convert
        self.rect = self.image.get_rect()


    pass

class Model:
    def __init__(self):
        self.all_penguins = pygame.sprite.Group()
        penguin = Penguin()
        penguin.rect.x = 15
        penguin.rect.y = 15
        self.all_penguins.add(penguin)

class Sled_Main:
    def __init__(self, size, model):
        pygame.init()
        size = (500, 400)
        self.WHITE = pygame.Color(255, 0, 0)
        self.screen = pygame.display.set_mode(size)

    def loadSprites(self):
        self.penguin = Penguin()
        self.all_penguins = pygame.sprite.RenderPlain(self.penguin)

    def main_loop(self):
        self.loadSprites()
        running = True
        while running:
            #self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False

            self.all_penguins.update()
            self.screen.fill(self.WHITE)
            self.all_penguins.draw(self.screen)
        pygame.quit()

class Obstacles(object):
    pass





if __name__ == '__main__':
    game = Sled_Main()
    game.main_loop()


    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             running = False
    #     time.sleep(.001)
    #
    # pygame.quit()
