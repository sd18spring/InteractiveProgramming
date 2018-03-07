import pygame
from pygame.locals import *
import time
import math
import random
class Asteroid():
    def __init__(self,x,y,speed,direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        #self.image = pygame.image.load('Asteroid.png').convert()
        #self.w, self.h = self.image.get_size()
    def update(self,gameDisplay):
        width, height = gameDisplay.get_size()
        self.x = self.x + (self.speed * math.cos(self.direction))
        self.y = self.y + (self.speed * math.sin(self.direction))
        if(self.x >= width):
            self.x = 0 - self.w
        elif(self.x <= 0 - self.w):
            self.x = width
        if(self.y >= height):
            self.y = 0 - self.h
        elif(self.y <= 0 - self.h):
            self.y = height
        gameDisplay.blit(self.image,(self.x,self.y))
class LargeAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        self.image = pygame.image.load('Asteroid.png').convert()
        self.w,self.h = self.image.get_size()
        super().__init__(x,y,speed,direction)
class MediumAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        self.image = pygame.image.load('Asteroid.png').convert()
        self.w,self.h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2))
        self.w,self.h = self.image.get_size()
        super().__init__(x,y,speed,direction)
class SmallAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        self.image = pygame.image.load('Asteroid.png').convert()
        self.w,self.h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,(self.w // 4,self.h // 4))
        self.w,self.h = self.image.get_size()
        super().__init__(x,y,speed,direction)

def spawnAsteroids(numberOfAsteroids,gameDisplay):
    width, height = gameDisplay.get_size()
    listOfAsteroids = []
    for i in numberOfAsteroids:
        side = random.randint(1,4)
        if(side == 1):
            x = random.randint(0,200)
            y = random.randint(0,height)
        elif(side == 2):
            x = random.randint(0,width)
            y = random.randint(0,200)
        elif(side == 3):
            x = random.randint(width-200,width)
            y = random.randint(0,height)
        elif(side == 4):
            x = random.randint(0,width)
            y = random.randint(height-200,height)
        random
        listOfAsteroids.append(LargeAsteroid)
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
Asteroid1 = SmallAsteroid(200,300,4,math.pi / 4)
BlackScreen = pygame.image.load('BlackScreen.jpg')
gameDisplay.blit(BlackScreen,(0,0))
for i in range(800):
    gameDisplay.blit(BlackScreen,(0,0))
    Asteroid1.update(gameDisplay)
    pygame.display.update()
    pygame.time.delay(20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
