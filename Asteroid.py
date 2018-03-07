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
        self.image = pygame.image.load('Asteroid.png').convert()
        self.image.set_colorkey((0,0,0))
        self.w, self.h = self.image.get_size()
        self.destroyed = False
    def update(self,gameDisplay):
        if(not self.destroyed):
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
        super().__init__(x,y,speed,direction)
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2))
        self.w,self.h = self.image.get_size()
    def destroy(self):
        self.destroyed = True
        MedAster = []
        for i in range(2):
            MedAster.append(MediumAsteroid(self.x,self.y,self.speed*2,random.uniform(0,2*math.pi)))
        return MedAster
class MediumAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        super().__init__(x,y,speed,direction)
        self.image = pygame.transform.scale(self.image,(self.w // 4,self.h // 4))
        self.w,self.h = self.image.get_size()
class SmallAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        super().__init__(x,y,speed,direction)
        self.image = pygame.transform.scale(self.image,(self.w // 8,self.h // 8))
        self.w,self.h = self.image.get_size()

def spawnAsteroids(numberOfAsteroids,gameDisplay,speed):
    width, height = gameDisplay.get_size()
    listOfAsteroids = []
    sampleAsteroid = LargeAsteroid(0,0,0,0)
    smallArea = 100
    for i in range(numberOfAsteroids):
        side = random.randint(1,4)
        if(side == 1):
            x = random.randint(-sampleAsteroid.w // 2,smallArea - sampleAsteroid.w // 2)
            y = random.randint(-sampleAsteroid.h // 2,height - sampleAsteroid.h // 2)
        elif(side == 2):
            x = random.randint(-sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
            y = random.randint(-sampleAsteroid.w // 2,smallArea - sampleAsteroid.w // 2)
        elif(side == 3):
            x = random.randint(width-smallArea - sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
            y = random.randint( -sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
        elif(side == 4):
            x = random.randint( -sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
            y = random.randint(height-smallArea - sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
        direction = random.uniform(0,math.pi * 2)
        listOfAsteroids.append(LargeAsteroid(x,y,speed,direction))
    return listOfAsteroids

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
#Asteroid1 = SmallAsteroid(200,300,4,math.pi / 4)
Asteroids = spawnAsteroids(6,gameDisplay,2)
BlackScreen = pygame.image.load('BlackScreen.jpg')
gameDisplay.blit(BlackScreen,(0,0))
for j in Asteroids:
    j.update(gameDisplay)
pygame.display.update()
pygame.time.delay(3000)
for i in range(400):
    gameDisplay.blit(BlackScreen,(0,0))
    #Asteroid1.update(gameDisplay)
    for j in Asteroids:
        j.update(gameDisplay)
    pygame.display.update()
    pygame.time.delay(20)
for k in Asteroids:
    Asteroids += k.destroy()
for i in range(400):
    gameDisplay.blit(BlackScreen,(0,0))
    #Asteroid1.update(gameDisplay)
    for j in Asteroids:
        j.update(gameDisplay)
    pygame.display.update()
    pygame.time.delay(20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
