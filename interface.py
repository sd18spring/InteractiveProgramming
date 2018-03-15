"""
Asteroids via Pygame

@authors coreyacl & nathanestill

"""

import pygame
from math import cos,sin,sqrt,radians,atan,pi
from classes import *
import time
import random


""" initiate pygame """
pygame.init()

""" initiate screen """
display_width = 1600
display_height = 1200
imgScale = .13
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Asteroids")
black = (0,0,0)
white = (255,255,255)

""" some other important things """
clock = pygame.time.Clock()
running = True

""" initiate ship object """
shipImg = pygame.image.load('spa1.png')
shipX = (display_width * .5)
shipY = (display_height * .5)
w,h = shipImg.get_size()
shipImg = pygame.transform.scale(shipImg,(int(w*imgScale),int(h*imgScale)))
ship = Ship(shipX,shipY,270,shipImg,gameDisplay)

""" initiate asteroids and UFOs """
numberOfAsteroids = 4
AllThings = listOfObjects(gameDisplay,ship)
AllThings.Asteroids.spawnAsteroids(numberOfAsteroids)
AllThings.UFOs.spawnBigUFO()
AllThings.update() # testing the many asteroids spawn in the right spot

""" initiate GUI """
gui = GUI(gameDisplay)

""" initialize the ship to be able to shoot"""
canShoot = True

while running:

    """ listens to events and does stuff """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # print(event)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                running = False
    """ player interface """
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        ship.move()
    else:
        ship.drift = True
    if keys_pressed[pygame.K_LEFT]:
        ship.rotate(1)
    if keys_pressed[pygame.K_RIGHT]:
        ship.rotate(-1)
    if(canShoot):
        counter = 0
    else:
        counter += 1
        if(counter >= 20):
            canShoot = True
    if keys_pressed[pygame.K_SPACE]:
        if(canShoot):
            ship.shoot(AllThings)
            canShoot = False
            counter = 0
    """ UFO spawning """
    randomInt = random.randint(1,1000)
    if(randomInt == 1 and len(AllThings.UFOs.listOfUFOs) == 0):
        AllThings.UFOs.spawnBigUFO()

    """ spawns new level """
    if(len(AllThings.Asteroids.listOfAsteroids) == 0 and len(AllThings.UFOs.listOfUFOs) == 0):
        numberOfAsteroids += 1
        AllThings.Asteroids.spawnAsteroids(numberOfAsteroids)



    gameDisplay.fill(black)
    gui.update(ship)
    ship.update()
    AllThings.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
