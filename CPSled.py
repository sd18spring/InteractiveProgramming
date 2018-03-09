#THIS FILE IS DOPE
import pygame
from pygame.locals import *
import time
clock = pygame.time.Clock()

class Penguin(pygame.sprite.Sprite): # code is from pygame documenta
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color
        self.image = pygame.image.load("penguin_smol.png")
        self.rect = self.image.get_rect()
    def moveUp(self, pixels):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y -= pixels

    def moveDown(self, pixels):
        if self.rect.y >= 340:
            self.rect.y = 340
        else:
            self.rect.y += pixels



class Obstacles(pygame.sprite.Sprite):
    def __init__(self, rect = None):
        super().__init__()
        self.image = pygame.image.load("rock.png")
        self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect

    def moveLeft(self, pixels):
        self.rect.x -= pixels
# class Model:
#     def __init__(self):
#         self.all_penguins = pygame.sprite.Group()
#         penguin = Penguin()


class Sled_Main:
    def __init__(self):
        pygame.init()
        size = (500, 400)
        self.WHITE = pygame.Color(255, 255, 255)
        self.screen = pygame.display.set_mode(size)

    def loadSprites(self):
        self.penguin = Penguin()
        self.all_penguins = pygame.sprite.RenderPlain(self.penguin)

        self.boulders = pygame.sprite.RenderPlain()
        self.boulders.add(Obstacles(pygame.Rect(100, 100, 60, 60)))

    def main_loop(self):
        self.loadSprites()
        running = True
        pygame.display.set_caption("Club Penguing Sledding Game")
        while running:
            #self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.penguin.moveUp(15)
            if keys[pygame.K_RIGHT]:
                self.penguin.moveDown(15)
            self.all_penguins.update()

            list_of_boulders = self.boulders.sprites()


            if self.penguin.rect.colliderect(list_of_boulders[0].rect):
                list_of_boulders[0].moveLeft(0)
            else:
                list_of_boulders[0].moveLeft(1)
            self.boulders.update()

            self.screen.fill(self.WHITE)
            self.boulders.draw(self.screen)
            self.all_penguins.draw(self.screen)
            pygame.display.update()
            clock.tick(60)
        pygame.quit()




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
