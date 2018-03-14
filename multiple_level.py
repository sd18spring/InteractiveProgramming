import pygame, sys
from pygame.locals import *
import time
from turtle import *
import os
dog = pygame.image.load('dog2.jpg')
space = pygame.image.load('space.png')
gameover = pygame.image.load('gameover.jpg')
youwin = pygame.image.load('win.jpg')
from random import *
import random as random


backgrounds = [dog,space]
class PyGameWindowView(object):

    def __init__(self, model, size, obstacles):


        self.screen = pygame.display.set_mode(size)
        self.model = model
        self.obstacles = obstacles

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))

######Line Drawing####
        self.lineStart = (0, 480)
        self.drawColor = (0, 0, 0)
        self.lineWidth = 10



    def draw(self):
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 255, 255),
                         pygame.Rect(self.model.x-20,
                                     self.model.y-20,
                                     self.model.width+20,
                                     self.model.height+20))

        pygame.draw.rect(self.screen,
                         pygame.Color(0, 0, 0),
                         pygame.Rect(self.model.x,
                                     self.model.y,
                                     self.model.width,
                                     self.model.height))



        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen,
                             pygame.Color(0, 0, 255),
                             pygame.Rect(obstacle.x,
                                         obstacle.y,
                                         obstacle.height,
                                         obstacle.width))

class Target(object):
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
    def __init__(self,x,y,height,width):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __str__(self):
        return "Obstacle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)


def create_newLevel(PyGameWindowView, Target, background, size):
    obstacles = []
    for i in range(random.randint(0,6)):
        obstacle = Obstacle(random.randint(120,1000),
                            random.randint(100,760),
                            random.randint(30,70),
                            random.randint(30,70))
        obstacles.append(obstacle)
    nextLevel = PyGameWindowView(target,size , obstacles)
    nextLevel.screen.blit(background, (0,0))


    pygame.display.update()
    return nextLevel, obstacles

if __name__ == '__main__':

    pygame.init()
    size = (1280,960)
    target = Target(size)
    obstacle = Obstacle(0,0,0,0)
    obstacles = []
    obstacles.append(obstacle)
    view = PyGameWindowView(target,size, obstacles)
    score = 0
    running = True
    view.screen.blit(view.background,(0,0))
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        lineEnd = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            mousex, mousey = pygame.mouse.get_pos()
            ####Line Drawing Code###
            pygame.draw.line(view.background, view.drawColor, view.lineStart, lineEnd, view.lineWidth)
            view.lineStart = lineEnd
            #####
            ### Collisions ###
            for obstacle in obstacles:
                if mousex in range(obstacle.x, obstacle.x+obstacle.width) and mousey in range(obstacle.y, obstacle.y+obstacle.height):
                    view.screen.blit(gameover, (0,0))
                    #pygame.quit()
            ###Leveling Up ###
            if mousex in range(target.x, target.x+target.width) and mousey in range(target.y, target.y+target.height):
                chosen_background =  random.choice(backgrounds) #setting a random background
                levelTwo, obstacles = create_newLevel(PyGameWindowView, target, chosen_background, size)
                view.background = chosen_background
                print(obstacles) #the obstacles will only show with this statement
                score += 1
                pygame.display.flip()
                pygame.display.update()
                levelTwo.draw()
                pygame.display.update()
                pygame.mouse.set_pos((0,480)) #resetting mouse position to the left most part of the screen
            if score == 5:
                view.screen.blit(youwin, (0,0))

        pygame.display.flip()
        pygame.display.update()
        view.draw()
        pygame.display.update()
        time.sleep(.001)
    pygame.quit()
