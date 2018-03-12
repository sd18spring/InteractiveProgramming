#!/usr/bin/env python
#
# Sling
# A game about the controlled destruction of fruits.
#
# Amy Phung // Sid Garimella
# Software Design 2017-2018, Olin College

VERSION = "0.1"
ASSET_DIRECTORY = "assets"
RESOLUTION_X = 1920
RESOLUTION_Y = 1080
G = -0.018

""" Loads all modules/dependencies.
"""

try:
    import sys
    import random
    import math
    import numpy as np
    import os
    import pygame
    from pygame.locals import *
except ImportError:
    print("Some dependencies are missing. Aborting...")
    sys.exit(2)


""" Resource Management/Utils
"""

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit
    return image, image.get_rect()


""" Game objects
"""

class Fruit(pygame.sprite.Sprite):
    """A generic, periodically generated on-screen target.
    Returns: fruit object
    """

    def __init__(self, type, vector):
        pygame.sprite.Sprite.__init__(self)
        self.type = type;
        self.image, self.rect = load_png(ASSET_DIRECTORY + '/' + str(type) + '.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = 400;
        self.rect.y = 1000;
        self.vector = vector

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self,rect,vector):
        # Work out low gravity toss physics
        self.vector = (vector[0]-G,vector[1])
        (angle,z) = vector
        print(angle*180/np.pi)
        # polar 2 cartesian
        (dx,dy) = (z*math.cos(angle%(2*np.pi)), z*math.sin((angle-G)%(2*np.pi)))
        return rect.move(dx,dy)


""" Main loop
"""

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Sling')

    # Fill background
    background = pygame.image.load('data/back1.png')
    background = background.convert()

    # Initialise players
    global player1


    # Initialise ball
    speed = 15
    rand = ((0.1 * (random.randint(5,8))))
    ball = Fruit('orange',(-1.62,speed))

    # Initialise sprites
    #playersprites = pygame.sprite.RenderPlain((player1))
    ballsprite = pygame.sprite.RenderPlain(ball)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Event loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        screen.blit(background, ball.rect, ball.rect)
        #screen.blit(background, player1.rect, player1.rect)

        ballsprite.update()

        if not 	(ball.rect.collidepoint(pygame.mouse.get_pos())):
	        #playersprites.update()
	        ballsprite.draw(screen)
	        #playersprites.draw(screen)
	        pygame.display.flip()


if __name__ == '__main__': main()
