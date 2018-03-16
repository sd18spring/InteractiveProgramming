import pygame
from pygame.locals import *
import time

# Define some colors
WHITE = (255, 255, 255) # have no idea what it does
BLACK = (0, 0, 0) # need to keep

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([600, 361])

clock = pygame.time.Clock() # I sure this controls the time the game (how faster the puase is at the bottom)

class Player(object): # player object right now is confusing do it postion here but not being used
    """ Encodes the state of the paddle in the game """
    def __init__(self):
        """ Initialize the player and position (x,y) """

        self.x = 0
        self.y = 0
        self.player_image = pygame.image.load("top_down_tank-8hkMRt.png").convert() #image goes here
        self.player_image.set_colorkey(BLACK)

    def update(self):# this may work idk yet
        """ update the state of the paddle """
        self.x += self.x
        self.y += self.y

    def __str__(self):
        return "Player, x=%f, y=%f" % (self.x, self.y)

class PyGameKeyboardController(object): #works well a little jumpy maybe use vx
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

# Load and set up graphics only back grond
background_image = pygame.image.load("GrassBackground.jpg").convert()


clock = pygame.time.Clock()
controller = PyGameKeyboardController()
player = Player()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        

    # Copy image to screen:
    screen.blit(background_image, background_position)


    controller.handle_event(event)
    player.update()



    # Copy image to screen:
    screen.blit(player.player_image, [controller.x, controller.y])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
