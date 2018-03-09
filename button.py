import pygame
import time
import math

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((250,250))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
            if event.type == pygame.QUIT:
                running = False
                break
            screen.fill(pygame.Color(28, 172, 229))
        pygame.display.update()


    pygame.quit()
