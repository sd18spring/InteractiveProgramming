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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.forward = True
            if event.key == pygame.K_LEFT:
                ship.ro = True
                ship.rdir = 1
            if event.key == pygame.K_RIGHT:
                ship.ro = True
                ship.rdir = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ship.ro = False
            if event.key == pygame.K_UP:
                ship.drift = True
                ship.forward = False
            if event.key == pygame.K_q:
                running = False

    gameDisplay.fill(black)
    gui.update(150000)
    ship.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
