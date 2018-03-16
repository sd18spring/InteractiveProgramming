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
    def __init__(self):
        """ Initialize the player and position (x,y) """

        self.x = 0
        self.y = 0
        self.player_image = pygame.image.load("RedTank.png").convert()
        self.player_image.set_colorkey(BLACK)
    def update(self):
        """ update the state of the paddle """
        self.x += self.x
        self.y += self.y

    def __str__(self):
        return "Player, x=%f, y=%f" % (self.x, self.y)

class PyGameKeyboardController(object):
    """ Handles keyboard input for brick breaker """
    def __init__(self):
       #self.model = model
       self.x = 0
       self.y = 0

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the paddle """
        #link for event.key https://www.pygame.org/docs/ref/key.html

        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.x += -10
        if event.key == pygame.K_RIGHT:
            self.x += 10
        if event.key == pygame.K_UP:
            self.y += -10
        if event.key == pygame.K_DOWN:
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
controller = PyGameKeyboardController()
player = Player()
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


    controller.handle_event(event)
    player.update()



    # Copy image to screen:
    screen.blit(player.player_image, [controller.x, controller.y])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
