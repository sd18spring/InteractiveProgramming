import pygame
from pygame.locals import *
import time
import math
import random
class Asteroid():
    def __init__(self,x,y,speed,direction,gameDisplay):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load('Asteroid.png').convert()
        self.image.set_colorkey((0,0,0)) # Sets the Asteroids Blackness to be transparent
        self.w, self.h = self.image.get_size() # Gets the Asteroid's width and height
        self.destroyed = False
        self.gameDisplay = gameDisplay
    def update(self):
        if(not self.destroyed): # once the asteroid is destroyed, it will stop redrawing the asteroid
            width, height = self.gameDisplay.get_size() # gets the display's width and length
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
            self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
            pygame.draw.rect(self.gameDisplay,(255,0,0),self.rect)
            self.gameDisplay.blit(self.image,(self.x,self.y)) # draws the asteroid on the screen
class LargeAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction,gameDisplay):
        super().__init__(x,y,speed,direction,gameDisplay)
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2)) # scales the asteroid to size
        self.w,self.h = self.image.get_size()
        self.shrinkage = 50
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
    def destroy(self):
        if(not self.destroyed):
            self.destroyed = True
            MedAster = []
            for i in range(2):
                MedAster.append(MediumAsteroid(self.x,self.y,self.speed*1.5,random.uniform(0,2*math.pi),self.gameDisplay)) #makes two more medium asteroids in it's place with random directions
            return MedAster
        return []
class MediumAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction,gameDisplay):
        super().__init__(x,y,speed,direction,gameDisplay)
        self.image = pygame.transform.scale(self.image,(self.w // 4,self.h // 4)) # half as big as large asteroid
        self.w,self.h = self.image.get_size()
        self.shrinkage = 25
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
    def destroy(self):
        if(not self.destroyed):
            self.destroyed = True
            SmallAster = []
            for i in range(2):
                SmallAster.append(SmallAsteroid(self.x,self.y,self.speed*1.5,random.uniform(0,2*math.pi),self.gameDisplay)) #makes two more medium asteroids in it's place with random directions
            return SmallAster
        return []
class SmallAsteroid(Asteroid):
    def __init__(self,x,y,speed,direction,gameDisplay):
        super().__init__(x,y,speed,direction,gameDisplay)
        self.image = pygame.transform.scale(self.image,(self.w // 8,self.h // 8)) # half as big as large asteroid
        self.w,self.h = self.image.get_size()
        self.shrinkage = 12
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
    def destroy(self):
        self.destroyed = True
        return []
class CollectionOfAsteroids():
    def __init__(self,gameDisplay,speed):
        self.listOfAsteroids = []
        self.gameDisplay = gameDisplay
        self.speed = speed
    def spawnAsteroids(self,numberOfAsteroids):
        width, height = self.gameDisplay.get_size()
        listOfAsteroids = [] # initializes a list of asteroids to update
        listOfRects = []
        sampleAsteroid = LargeAsteroid(0,0,0,0,self.gameDisplay) # a sample asteroid to know where to spawn the asteroids in case we change the size later
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
                y = random.randint(-sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
            elif(side == 4): # bottom of the screen
                x = random.randint(-sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
                y = random.randint(height-smallArea - sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
            direction = random.uniform(0,math.pi * 2) # initiate each asteroid with a random direction
            listOfAsteroids.append(LargeAsteroid(x,y,self.speed,direction,self.gameDisplay))
            listOfRects.append(listOfAsteroids[i].rect)
        self.listOfAsteroids = listOfAsteroids
        self.listOfRects = listOfRects
    def update(self):
        listOfRects = []
        ListToDelete = []
        for i in range(len(self.listOfAsteroids)):
            if(self.listOfAsteroids[i].destroyed):
                ListToDelete.append(i)
            else:
                self.listOfAsteroids[i].update()
                listOfRects.append(self.listOfAsteroids[i].rect)
        for j in reversed(ListToDelete):
            del self.listOfAsteroids[j]
        self.listOfRects = listOfRects
    def destroyAll(self):
        sizeOfAsteroids = range(len(self.listOfAsteroids))
        for i in sizeOfAsteroids:
            newAsteroid = self.listOfAsteroids[i].destroy()
            if(newAsteroid != None):
                self.listOfAsteroids += newAsteroid # destroying all of the asteroids making them medium
        for i in sizeOfAsteroids:
            self.listOfAsteroids.pop(0)
class Projectile():
    def __init__(self,x,y,direction,gameDisplay):
        size = 3
        self.x = x
        self.y = y
        self.w = size
        self.h = size
        self.speed = 10
        self.direction = direction
        self.rect = ((self.x,self.y),(size,size))
        self.image = pygame.Surface((size,size))
        self.image.fill((255,255,255))
        self.gameDisplay = gameDisplay
        self.destroyed = False
        self.distanceTravelled = 0
        self.distanceWanted = 500
    def update(self):
        if(self.distanceTravelled < self.distanceWanted): # once the asteroid is destroyed, it will stop redrawing the asteroid
            width, height = self.gameDisplay.get_size() # gets the display's width and length
            self.x = self.x + (self.speed * math.cos(self.direction))  # Sets the Asteroid's to a small change in space
            self.y = self.y + (self.speed * math.sin(self.direction))
            self.distanceTravelled += self.speed
            if(self.x >= width): # If the asteroid's coordinate goes outside of the window, set that coordinate to the other side of the map
                self.x = 0 - self.w  # adding the width of the image to make sure that the image doesn't appear suddenly (the image's position is the top right of the image)
            elif(self.x <= 0 - self.w): # same as above (makes it so that the whole image has to leave the screen for it to go to the other side)
                self.x = width
            if(self.y >= height):
                self.y = 0 - self.h
            elif(self.y <= 0 - self.h):
                self.y = height
            self.rect = pygame.Rect((self.x,self.y),(self.w,self.h))
            pygame.draw.rect(self.gameDisplay,(0,255,0),self.rect)
            self.gameDisplay.blit(self.image,(self.x,self.y)) # draws the asteroid on the screen
        else:
            self.destroy()
    def destroy(self):
        self.destroyed = True
class CollectionOfProjectiles():
    def __init__(self,gameDisplay):
        self.listOfProjectiles = []
        self.listOfRects = []
        self.gameDisplay = gameDisplay
    def addProjectile(self,x,y,direction):
        self.listOfProjectiles.append(Projectile(x,y,direction,self.gameDisplay))
    def update(self):
        print(len(self.listOfProjectiles))
        ListToDelete = []
        for i in range(len(self.listOfProjectiles)):
            if(self.listOfProjectiles[i].destroyed):
                ListToDelete.append(i)
            else:
                self.listOfProjectiles[i].update()
        for j in reversed(ListToDelete):
            del self.listOfProjectiles[j]
class listOfObjects():
    def __init__(self,asteroids,proj):
        self.Asteroids = asteroids
        self.Projectiles = proj
    def update(self):
        self.Projectiles.update()
        self.Asteroids.update()
        print(len(self.Asteroids.listOfAsteroids),len(self.Asteroids.listOfRects))
        for i in self.Projectiles.listOfProjectiles:
            collisions = i.rect.collidelist(self.Asteroids.listOfRects)
            if (collisions != -1):
                self.Asteroids.listOfAsteroids += self.Asteroids.listOfAsteroids[collisions].destroy()
                i.destroy()


pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
numberOfAsteroids = 4
CollAster = CollectionOfAsteroids(gameDisplay,1)
CollAster.spawnAsteroids(numberOfAsteroids) # initiating a list of asteroids to keep track of
proj = CollectionOfProjectiles(gameDisplay)
proj.addProjectile(400,300,math.pi / 4)
Black = (0,0,0) # black screen is the background
gameDisplay.fill(Black)
AllThings = listOfObjects(CollAster,proj)
AllThings.update() # testing the many asteroids spawn in the right spot
pygame.display.update()
running = True # for the exit of the game
randomCounter = 0
while running:
    randomCounter += 1
    if(randomCounter % 50 == 0):
        AllThings.Projectiles.addProjectile(400,300,random.uniform(0,2*math.pi))
    gameDisplay.fill(Black)
    AllThings.update()# update each asteroid
    #proj.update()
    pygame.display.update()
    if(len(AllThings.Asteroids.listOfAsteroids) == 0):
        numberOfAsteroids += 1
        AllThings.Asteroids.spawnAsteroids(numberOfAsteroids)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                running = False
pygame.quit()
