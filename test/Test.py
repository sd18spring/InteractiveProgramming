"""
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/4YqIKncMJNs
 Explanation video: http://youtu.be/ONAK8VZIcI4
 Explanation video: http://youtu.be/_6c4o41BIms
"""

import pygame
from pygame.locals import *
import time

# Define some colors
#WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 1024x768 sized screen
screen = pygame.display.set_mode([1024, 768])

# This sets the name of the window
# pygame.display.set_caption('CMSC 150 is cool')

clock = pygame.time.Clock()

class Player(object):
    """ Encodes the state of the paddle in the game """
    def __init__(self, filename, x, y):
        """ Initialize the player and position (x,y) """

        self.x = x
        self.y = y
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)
    def update(self):
        """ update the state of the paddle """
        self.x += self.x
        self.y += self.y

    def __str__(self):
        return "Player, x=%f, y=%f" % (self.x, self.y)

class PyGameKeyboardController(object):
    """ Handles keyboard input tanks """
    def __init__(self, u, d, l, r):
       #self.model = model
       self.x = 0
       self.y = 0
       self.l = self.l
       self.d = self.d
       self.u = self.u
       self.r = self.r
    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the tank """
        #link for event.key https://www.pygame.org/docs/ref/key.html

        if event.type != KEYDOWN:
            return
        if event.key == self.l:
            self.x += -10
        if event.key == self.r:
            self.x += 10
        if event.key == self.u:
            self.y += -10
        if event.key == self.d:
            self.y += 10
# Before the loop, load the sounds:
#click_sound = pygame.mixer.Sound("laser5.ogg")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
background_image = pygame.image.load("NewBackground.jpg").convert()
# player_image = pygame.image.load("top_down_tank-8hkMRt.png").convert()
# player_image.set_colorkey(BLACK)

clock = pygame.time.Clock()
controller1 = PyGameKeyboardController(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
controller2 = PyGameKeyboardController('K_w', 'K_s', 'K_a', 'K_d')

player1 = Player("BlueTank.png", 0, 0)
player2 = Player("RedTank.png", 100, 100)
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     click_sound.play()
        #if event.type != KEYDOWN:

    # Copy image to screen:
    screen.blit(background_image, background_position)


    controller1.handle_event(event)
    controller2.handle_event(event)
    player1.update()
    player2.update()



    # Copy image to screen:
    screen.blit(player1.player_image, [controller1.x, controller1.y])
    screen.blit(player2.player_image, [controller2.x, controller2.y])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
