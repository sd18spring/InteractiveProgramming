"""
List of things we used so far: Brian Wilkinson (Youtube video about...sprites and stuff)
"""
import pygame, sys
from pygame.locals import *
import random

SCREENWIDTH = 1500
SCREENHEIGHT = 1000

def main():
    pygame.init()

    mainSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
    pygame.display.set_caption("Yes I do.")
    blocksGroup = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    score = 0

    for i in range(10):
        height = random.randint(30, 150)
        weight = random.randint(30, 150)
        myBlock = Block(mainSurface, (255, 255, 255), weight, height)
        x_displacement = random.randint(0, SCREENWIDTH)
        myBlock.rect.x = (SCREENWIDTH + x_displacement)
        myBlock.rect.y = random.randrange(SCREENHEIGHT - 150)
        blocksGroup.add(myBlock)

    player = Player(mainSurface, (255, 0, 0))
    player.rect.x = 200
    player.rect.y = 0.5*SCREENHEIGHT
    player_group.add(player)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print(score)
                pygame.quit()
                sys.exit()

            player.on_event(event)
        mainSurface.fill((0, 0, 0))

        player.collide(blocksGroup, score)

        player_group.draw(mainSurface)
        blocksGroup.update()
        blocksGroup.draw(mainSurface)
        pygame.display.update()
        score += .01


class Block(pygame.sprite.Sprite):
    def __init__(self, screen, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.speedx = 2

    def update(self):
        self.rect.left -= self.speedx
        if self.rect.right < 0:
            x_displacement = random.randint(0, SCREENWIDTH*2)
            self.rect.x = (SCREENWIDTH + x_displacement)
            self.rect.y = random.randrange(SCREENHEIGHT - 150)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()

    def on_event(self, event):
        if event.type == KEYDOWN:

            if self.rect.y > SCREENHEIGHT-75:
                self.rect.y = SCREENHEIGHT - 50
            elif self.rect.y < SCREENHEIGHT- 50:
                self.rect.y += 20



        elif event.type == MOUSEBUTTONDOWN:
            if self.rect.y < 25:
                self.rect.y = 0
            elif self.rect.y > 0:
                self.rect.y -= 20

    def collide(self, obstacles, score):
        if pygame.sprite.spritecollide(self, obstacles, False):
            print(int(score))
            pygame.quit()
            sys.exit()




main()
