import pygame, sys
from pygame.locals import *
import time
from turtle import *
import os
from random import *
import random as random

dog = pygame.image.load('dog2.jpg')
space = pygame.image.load('space.png')
wave = pygame.image.load('wave.jpg')
sky = pygame.image.load('sky.jpg')
mountain = pygame.image.load('mountain.jpg')
gameover = pygame.image.load('gameover.jpg')
youwin = pygame.image.load('win.jpg')
horsey = pygame.image.load('horsey2.jpg')
horsey.set_colorkey((255,255,255))
carrot = pygame.image.load('carrot2.png')
carrot.set_colorkey((255,255,255))
horsey_rect = horsey.get_rect()
carrot_rect = carrot.get_rect()

backgrounds = [dog,space, wave,sky]
class PyGameWindowView(object):

    def __init__(self, target, size):


        self.screen = pygame.display.set_mode(size)
        self.target = target

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))

    def draw(self):

        ##Target Border##
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 255, 255),
                         pygame.Rect(self.target.x-20,
                                     self.target.y-20,
                                     self.target.width+20,
                                     self.target.height+20))
        ##Target ##
        pygame.draw.rect(self.screen,
                         pygame.Color(0, 0, 0),
                         pygame.Rect(self.target.x,
                                     self.target.y,
                                     self.target.width,
                                     self.target.height))


class Target(object):
    """Initializing the "goal" for the player
    """
    def __init__(self, size):
        self.height = 100
        self.width = 50
        self.x = 1230
        self.y = 480

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                            self.y)

class Obstacle(object):
    """Initializing an obstacle.
    """
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill((150, 60, 10))
        self.pos = pygame.math.Vector2(random.randrange(1230),
                                   random.randrange(910))
        self.vel = pygame.math.Vector2(random.uniform(-10, 10),
                                   random.uniform(-10, 10))

    def __str__(self):
        return "Obstacle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)

    def update(self):
        self.pos += self.vel
        if self.pos[0] < 50:
            #self.pos[0] += 50
            self.vel = (random.randint(1, 10), random.randint(1,10))
        if self.pos[0] > 1230:
            #self.pos[0] -= 50
            self.vel = (random.randint(-10, -1), random.randint(-10,-1))
        if self.pos[1] < 50:
            #self.pos[1] += 50
            self.vel = (random.randint(1, 10), random.randint(1,10))
        if self.pos[1] > 750:
            #self.pos[1] -= 50
            self.vel = (random.randint(-10, -1), random.randint(-10,-1))

def create_newLevel(PyGameWindowView, Target, background, size):
    """This function creates a whole new background with different
    obstacles for the next level."""
    obstacles = []
    for i in range(random.randint(0,10)):
        obstacle = Obstacle()
        obstacles.append(obstacle)
    nextLevel = PyGameWindowView(target,size)
    nextLevel.screen.blit(background, (0,0))
    for obstacle in obstacles:
        obstacle.update()
        nextLevel.screen.blit(obstacle.image, obstacle.pos)

    pygame.display.update()
    return nextLevel, obstacles

if __name__ == '__main__':

    pygame.init()
    size = (1280,960)
    target = Target(size)

    obstacles = []
    obstacle = Obstacle()
    obstacles.append(obstacle)
    view = PyGameWindowView(target,size)
    score = 0
    running = True
    view.screen.blit(view.background,(0,0))
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False


        #if pygame.mouse.get_pressed() == (1, 0, 0):
            ##setting mouse to be a carrot and the horse to follow##
            mousex, mousey = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)



            ### Collisions ###
            for obstacle in obstacles:
                if range(horsey_rect.left, horsey_rect.right) in range(int(obstacle.pos[0]), int(obstacle.pos[0]+50)) and range(horsey_rect.bottom, horsey_rect.top) in range(int(obstacle.pos[1]), int(obstacle.pos[1]+50)):
                    view.screen.blit(gameover, (0,0))

            ###Leveling Up ###
            if mousex in range(target.x, target.x+target.width) and mousey in range(target.y, target.y+target.height):
                chosen_background =  random.choice(backgrounds) #setting a random background
                levelTwo, obstacles = create_newLevel(PyGameWindowView, target, chosen_background, size)
                view.background = chosen_background
                score += 1
                pygame.display.flip()
                pygame.display.update()
                levelTwo.draw()
                pygame.display.update()
                pygame.mouse.set_pos((0,480)) #resetting mouse position to the left most part of the screen
            if score == 5:
                view.screen.blit(youwin, (0,0))
        view.screen.blit(view.background,(0,0))
        view.screen.blit(carrot, (mousex+30, mousey+30))
        view.screen.blit(horsey, (mousex-500, mousey))
        for obstacle in obstacles:
            obstacle.update()
            view.screen.blit(obstacle.image, obstacle.pos)
        pygame.display.flip()
        view.draw()
        pygame.display.update()
        time.sleep(.001)
    pygame.quit()
