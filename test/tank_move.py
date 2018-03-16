import pygame
from pygame.locals import *
import time

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# This sets the name of the window
pygame.display.set_caption('CMSC 150 is cool')

clock = pygame.time.Clock()

# Before the loop, load the sounds:
#click_sound = pygame.mixer.Sound("laser5.ogg")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
background_image = pygame.image.load("GrassBackground.jpg").convert()
player = pygame.image.load("top_down_tank-8hkMRt.png").convert()
player.set_colorkey(BLACK)
done = False
class PyGameKeyboardController(object):
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the paddle """
        #link for event.key https://www.pygame.org/docs/ref/key.html
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.player.position.x += -1
        if event.key == pygame.K_RIGHT:
            self.player.position.x += 1
        if event.key == pygame.K_UP:
            self.player.position.y += -1
        if event.key == pygame.K_DOWN:
            self.player.position.y += 1
controller = PyGameKeyboardController(player)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     click_sound.play()

    # Copy image to screen:
    screen.blit(background_image, background_position)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    controller.handle_event(event)
    x = player.position.x
    y = player.position.y

    # Copy image to screen:
    screen.blit(player, [x, y])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
