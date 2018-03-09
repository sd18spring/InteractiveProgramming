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
        self.image.set_colorkey((0,0,0)) # Sets the Asteroids Blackness to be transparent
        self.w, self.h = self.image.get_size() # Gets the Asteroid's width and height
        self.destroyed = False
    def update(self,gameDisplay):
        if(not self.destroyed): # once the asteroid is destroyed, it will stop redrawing the asteroid
            width, height = gameDisplay.get_size() # gets the display's width and length
            self.x = self.x + (self.speed * math.cos(self.direction))  # Sets the Asteroid's to a small change in space
            self.y = self.y + (self.speed * math.sin(self.direction))
            if(self.x >= width): # If the asteroid's coordinate goes outside of the window, set that coordinate to the other side of the map
                self.x = 0 - self.w  # adding the width of the image to make sure that the image doesn't appear suddenly (the image's position is the top right of the image)
            elif(self.x <= 0 - self.w): # same as above (makes it so that the whole image has to leave the screen for it to go to the other side)
                self.x = width
            if(self.y >= height):
                self.y = 0 - self.h
            elif(self.y <= 0 - self.h):
                self.y = height
            gameDisplay.blit(self.image,(self.x,self.y)) # draws the asteroid on the screen
class LargeAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        super().__init__(x,y,speed,direction)
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2)) # scales the asteroid to size
        self.w,self.h = self.image.get_size()
    def destroy(self):
        self.destroyed = True
        MedAster = []
        for i in range(2):
            MedAster.append(MediumAsteroid(self.x,self.y,self.speed*2,random.uniform(0,2*math.pi))) #makes two more medium asteroids in it's place with random directions
        return MedAster
class MediumAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        super().__init__(x,y,speed,direction)
        self.image = pygame.transform.scale(self.image,(self.w // 4,self.h // 4)) # half as big as large asteroid
        self.w,self.h = self.image.get_size()
class SmallAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction):
        super().__init__(x,y,speed,direction)
        self.image = pygame.transform.scale(self.image,(self.w // 8,self.h // 8)) # half as big as large asteroid
        self.w,self.h = self.image.get_size()

def spawnAsteroids(numberOfAsteroids,gameDisplay,speed):
    width, height = gameDisplay.get_size()
    listOfAsteroids = [] # initializes a list of asteroids to update
    sampleAsteroid = LargeAsteroid(0,0,0,0) # a sample asteroid to know where to spawn the asteroids in case we change the size later
    smallArea = 100 # the area that asteroids are to spawn around the the edge
    for i in range(numberOfAsteroids):
        side = random.randint(1,4)
        if(side == 1): # left side of the screen
            x = random.randint(-sampleAsteroid.w // 2,smallArea - sampleAsteroid.w // 2)
            y = random.randint(-sampleAsteroid.h // 2,height - sampleAsteroid.h // 2)
        elif(side == 2): # top side of the screen
            x = random.randint(-sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
            y = random.randint(-sampleAsteroid.w // 2,smallArea - sampleAsteroid.w // 2)
        elif(side == 3): # right side of the screen
            x = random.randint(width-smallArea - sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
            y = random.randint( -sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
        elif(side == 4): # bottom of the screen
            x = random.randint( -sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
            y = random.randint(height-smallArea - sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
        direction = random.uniform(0,math.pi * 2) # initiate each asteroid with a random direction
        listOfAsteroids.append(LargeAsteroid(x,y,speed,direction))
    return listOfAsteroids

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
#Asteroid1 = SmallAsteroid(200,300,4,math.pi / 4)
Asteroids = spawnAsteroids(6,gameDisplay,2) # initiating a list of asteroids to keep track of
BlackScreen = pygame.image.load('BlackScreen.jpg') # black screen is the background
gameDisplay.blit(BlackScreen,(0,0))
for j in Asteroids:
    j.update(gameDisplay) # testing the many asteroids spawn in the right spot
pygame.display.update()
pygame.time.delay(3000)
for i in range(400):
    gameDisplay.blit(BlackScreen,(0,0))
    #Asteroid1.update(gameDisplay)
    for j in Asteroids:
        j.update(gameDisplay) # update each asteroid
    pygame.display.update()
    pygame.time.delay(20)
for k in Asteroids:
    Asteroids += k.destroy() # destroying all of the asteroids making them medium
for i in range(400):
    gameDisplay.blit(BlackScreen,(0,0))
    #Asteroid1.update(gameDisplay)
    for j in Asteroids:
        j.update(gameDisplay) # reupdate everything
    pygame.display.update()
    pygame.time.delay(20)
running = True # for the exit of the game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
