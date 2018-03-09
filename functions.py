import pygame, sys, random
from pygame.locals import *
from classes import Player, Block

SCREENWIDTH = 1500
SCREENHEIGHT = 1000

def main():
    pygame.init()

    mainSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
    pygame.display.set_caption("Collision Game")
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

    player = Player(mainSurface, (255, 0, 0), 50, 20)
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
