import pygame
from pygame.locals import *
pygame.init()
SCREENRECT = Rect(0, 0, 640, 480)
background = [pygame.image.load('GrassBackground.jpg'),pygame.image.load('GrassBackground.jpg')]
screen_width=700
screen_height=400
screen=pygame.display.set_mode([screen_width,screen_height])
for i in range(6):
    screen.blit(background[i], (i*1, 0))
playerpos = 3
screen.blit(playerimage, (playerpos*10, 0))