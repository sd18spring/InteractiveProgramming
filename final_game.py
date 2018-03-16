import pygame, sys
from pygame.locals import *
import time
import os
from random import *
import random as random
from pygame import mixer
youwin0 = pygame.image.load('win.png')
gameover0 = pygame.image.load('lose.png')
background = pygame.image.load('underwater.jpg')
mainfish0 = pygame.image.load('mainfish.png')
mainfish0.set_colorkey((255,255,255))
trash0 = pygame.image.load('trash2.png')
food0 = pygame.image.load('target.png')

class PyGameWindowView(object):
    """This class initializes the background, sets the screen, and converts image formats for spped"""

    def __init__(self, target, size):


        self.screen = pygame.display.set_mode(size)
        youwin =youwin0.convert_alpha()
        mainfish = mainfish0.convert_alpha()
        trash = trash0.convert_alpha()
        food = food0.convert_alpha()
        gameover = gameover0.convert_alpha()

        self.target = target

        self.background1 = pygame.Surface(self.screen.get_size())
        self.background1.fill((255, 255, 255))

class Target(object):
    """Initializing the "goal" for the player to drag the fish to
    """
    def __init__(self, size):
        self.image = pygame.Surface((100,100))
        self.pos = (1230,480)
        self.height = 70
        self.width = 70
        self.x = 1140
        self.y = 800

    def __str__(self):
        return "Target height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                            self.y)

class Obstacle(object):
    """Initializing an obstacle for collison.
    """
    def __init__(self):
        self.image = pygame.Surface((90, 90))
        self.image.fill((150, 60, 10))
        self.image.set_colorkey((150,60,10))
        self.pos = pygame.math.Vector2(random.randrange(1230),
                                   random.randrange(910))
        self.vel = pygame.math.Vector2(random.uniform(-10, 10),
                                   random.uniform(-10, 10))

    def __str__(self):
        return "Obstacle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)

    def update(self, stop):
        #prevents obstacle from leaving pygame window
        self.pos += self.vel
        if self.pos[0] < 50:
            self.vel = (random.randint(1, 5), random.randint(1,5))
        if self.pos[0] > 1230:
            self.vel = (random.randint(-5, -1), random.randint(-5,-1))
        if self.pos[1] < 50:
            self.vel = (random.randint(1, 5), random.randint(1,5))
        if self.pos[1] > 960:
            self.vel = (random.randint(-5, -1), random.randint(-5,-1))

        if stop == True:
            self.vel = (0,0)


def create_newLevel(PyGameWindowView, Target, background, size):
    """This function creates a whole new background with different
    obstacles for the next level."""
    obstacles = []
    for i in range(random.randint(1,7)):
        obstacle = Obstacle()
        obstacles.append(obstacle)
    nextLevel = PyGameWindowView(target,size)
    nextLevel.screen.blit(background, (0,0))
    for obstacle in obstacles:
        obstacle.update(stop = False)
        nextLevel.screen.blit(obstacle.image, obstacle.pos)

    pygame.display.update()
    return nextLevel, obstacles

if __name__ == '__main__':

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    size = (1280,960)
    target = Target(size)

    obstacles = []
    obstacle = Obstacle()
    obstacles.append(obstacle)

    view = PyGameWindowView(target,size)
    view.background = background


    score = 0
    running = True
    view.screen.blit(view.background,(0,0))


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:

                mousex, mousey = pygame.mouse.get_pos()
                pygame.mouse.set_visible(False)

                view.screen.blit(view.background,(0,0))

                view.screen.blit(mainfish0, (mousex-100, mousey-100))
                view.screen.blit(food0, (1280-257,960-269) )


                for obstacle in obstacles:
                    obstacle.update(stop = False)
                    view.screen.blit(obstacle.image, obstacle.pos)
                    view.screen.blit(trash0,obstacle.pos)

                ### Collisions ###
                for obstacle in obstacles:
                    if abs(obstacle.pos[0]-mousex) <= 40:
                        if abs(obstacle.pos[1]-mousey) <= 65:
                            obstacle.update(stop=True)
                            view.screen.blit(gameover0, (0,0))
                            pygame.event.set_blocked(pygame.MOUSEMOTION)
                            pygame.event.set_allowed(pygame.KEYDOWN)
                            pygame.mixer.music.load('smack.mp3')
                            pygame.mixer.music.play()




                ###Leveling Up ###
                if mousex in range(target.x, target.x+target.width) and mousey in range(target.y, target.y+target.height):
                    pygame.mixer.music.load('bubble.mp3')
                    pygame.mixer.music.play()
                    levelTwo, obstacles = create_newLevel(PyGameWindowView, target, background, size)
                    score += 1
                    pygame.display.update()
                    pygame.mouse.set_pos((0,200)) #resetting mouse position to the left most part of the screen
                if score == 5:
                    view.screen.blit(youwin0, (0,0))
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    time.sleep(3)
                    #running = False

            ## You Lost Screen Options###
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    print('pressed')
                    running = False
                if event.key == K_SPACE:
                    print('pressed')
                    pygame.event.set_allowed(MOUSEMOTION)
                    event.type == MOUSEMOTION
                    levelTwo, obstacles = create_newLevel(PyGameWindowView, target, background, size)

                    pygame.mouse.set_pos((0,200)) #resetting mouse position to the left most part of the screen
                    mousex, mousey = pygame.mouse.get_pos()
                    pygame.mouse.set_visible(False)
                    view.screen.blit(view.background,(0,0))

                    view.screen.blit(mainfish0, (mousex-100, mousey-100))
                    view.screen.blit(food0, (1280-257,960-269) )
                    pygame.display.update()
        pygame.display.update()
        time.sleep(.001)
    pygame.quit()
