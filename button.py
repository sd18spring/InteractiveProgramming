from pygame.locals import *
import pygame
import pygame_textinput
import time
import math

if __name__ == '__main__':

    textinput = pygame_textinput.TextInput()


    pygame.init()
    screen = pygame.display.set_mode((250,250))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == pygame.QUIT:
                running = False
                break
            screen.fill(pygame.Color(28, 172, 229))
        # Feed it with events every frame
        textinput.update(pygame.event.get())
    # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (10, 10))

        pygame.display.update()


    pygame.quit()
