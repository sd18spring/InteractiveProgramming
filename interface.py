"""
Asteroids via Pygame

@authors coreyacl & nathanestill

"""

import pygame
from math import cos,sin,sqrt,radians,atan
from classes import *


pygame.init()

display_width = 1000
display_height = 800
imgScale = .2

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Asteroids")

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
running = True
shipImg = pygame.image.load('spa1.png')

shipX = (display_width * .5)
shipY = (display_height * .5)
w,h = shipImg.get_size()
shipImg = pygame.transform.scale(shipImg,(int(w*imgScale),int(h*imgScale)))
ship = Ship(shipX,shipY,270,shipImg,gameDisplay)

gui = GUI(gameDisplay)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # print(event)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                running = False
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP]:
        ship.move()
    else:
        ship.drift = True
    if keys_pressed[pygame.K_LEFT]:
        ship.rotate(1)
    if keys_pressed[pygame.K_RIGHT]:
        ship.rotate(-1)

    gameDisplay.fill(black)
    gui.update(150000)
    ship.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
