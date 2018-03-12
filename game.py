#!/usr/bin/env python
#
# Sling
# A game about the controlled destruction of fruits.
#
# Amy Phung // Sid Garimella
# Software Design 2017-2018, Olin College

VERSION = "0.1"
ASSET_DIRECTORY = "assets"
RESOLUTION_X = 1000
RESOLUTION_Y = 800

ORANGE = (244, 167, 66)
GREEN = (70, 170, 73)
RED = (168, 11, 69)
YELLOW = (249, 242, 17)

BACK = (56, 30, 0)

G = 0.01
colors = [ORANGE,GREEN,RED,YELLOW]
nowFruits = []
sizeMN = 30
sizeMX = 60

""" Loads all modules/dependencies.
"""

try:
    import sys
    import random
    import math
    import numpy as np
    import os
    import pygame
    from pygame.locals import *
except ImportError:
    print("Some dependencies are missing. Aborting...")
    sys.exit(2)


""" Game objects
"""

class Fruit(pygame.sprite.Sprite):
    """A periodically generated on-screen target.
    Returns: fruit object
    """

    def __init__(self, radius, color, vector):
        self.radius = radius
        self.color = color
        self.visible = 1
        self.vx = 0
        self.vy = 0
        self.x,self.y = vector
        self.drag = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy


pygame.init()
display_a = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
pygame.display.set_caption("Sling")
display_a.fill(BACK)

mainWindow = pygame.Rect(15,15,RESOLUTION_X - 30, RESOLUTION_Y - 30)
origin = pygame.Rect(RESOLUTION_X/2 - 100, RESOLUTION_Y - 30, 190, 30)

def generateNewBall() :
    radius = random.randint(sizeMN, sizeMX)
    center = ( origin.centerx, origin.centery)
    newBall = Fruit(radius, colors[random.randint(1,4) - 1], center)
    newBall.vy = -1*random.randint(4, 6)/3
    newBall.vx = random.randint(-2, 2)/5
    nowFruits.append(newBall)

def genWaveBalls():
    if len(nowFruits) == 0:
        for i in range(3):
            generateNewBall()
        for fruit in nowFruits:
            fruit.move()
            fruit.vy = fruit.vy + fruit.drag
            fruit.drag = fruit.drag + G*0.002
            if fruit.y < RESOLUTION_Y:
                pygame.draw.circle(display_a, fruit.color, (int(fruit.x), int(fruit.y)), fruit.radius, 0)
    else:
        for fruit in nowFruits:
            fruit.move()
            fruit.vy = fruit.vy + fruit.drag
            fruit.drag = fruit.drag + G*0.002
            if fruit.y < RESOLUTION_Y:
                pygame.draw.circle(display_a, fruit.color, (int(fruit.x), int(fruit.y)), fruit.radius, 0)
            elif fruit.y > 15000:
                nowFruits.clear()

def isOnFruit(vector):
    x,y = vector
    for fruit in nowFruits:
        if math.pow(x-fruit.x,2) + math.pow(y-fruit.y,2) < math.pow(fruit.radius,2):
            return fruit
    return False

""" Main loop
"""


pygame.mouse.set_cursor(*pygame.cursors.diamond)

while True:
    display_a.fill((255,255,255))
    pygame.draw.rect(display_a, BACK, mainWindow)
    genWaveBalls()

    event = pygame.event.poll()

    if event.type == pygame.MOUSEMOTION:
        currx, curry = event.pos
        if isOnFruit((currx,curry)) is not False:
            nowFruits.remove(isOnFruit((currx,curry)))

    if event.type == pygame.MOUSEBUTTONDOWN:
        x1, y1 = event.pos


    if event.type == pygame.MOUSEBUTTONUP:
        x2, y2 = event.pos


    pygame.display.update()
