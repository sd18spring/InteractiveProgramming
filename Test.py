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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([600, 361])

# This sets the name of the window
pygame.display.set_caption('CMSC 150 is cool')

clock = pygame.time.Clock()
y = 0
x = 0

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
            self.x += -1
        if event.key == pygame.K_RIGHT:
            self.x += 1
        if event.key == pygame.K_UP:
            self.y += -1
        if event.key == pygame.K_DOWN:
            self.y += 1
# Before the loop, load the sounds:
#click_sound = pygame.mixer.Sound("laser5.ogg")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
background_image = pygame.image.load("GrassBackground.jpg").convert()
player_image = pygame.image.load("top_down_tank-8hkMRt.png").convert()
player_image.set_colorkey(BLACK)
controller = PyGameKeyboardController()
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
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    # player_position = pygame.mouse.get_pos()
    # x = player_position[0]
    # y = player_position[1]


    # Copy image to screen:
    screen.blit(player_image, [controller.x, controller.y])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
