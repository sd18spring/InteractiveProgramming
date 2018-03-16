import pygame
from pygame.locals import *
import time
pygame.init()
screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
background_image = pygame.image.load("GrassBackground.jpg").convert()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            done = True
        screen.blit(background_image,[0,0])
        pygame.display.flip()
clock.tick(60)
pygame.quit()