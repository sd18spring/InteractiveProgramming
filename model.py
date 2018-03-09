import character
import terrain
import random
import pygame
from pygame.locals import *

class Model:
    def __init__(self, *args):
        self.game_running = True
        self.g = 15
        self.terrains = []
        self.characters = []

        for char in args:
            self.characters.append(char)

        #NOTE: Why is this a double for loop? We should just have one terrain
        #object for the ground, not 30.
        for i in range(10):
            for j in range(3):
                self.terrains.append(terrain.Terrain((i * 100,1000 - j * 100)))
        #for i in range(10):
        #    if(random.randint(1,2) == 2):
        #        self.terrains.append(terrain.Terrain((i * 100,1000 - 3 * 100)))

    def x_movement(self, event, game_object):
        """
        Toggles the different modes of acceleration depending on key up
        events and key down events.
        """
        if not (event.type == KEYDOWN or event.type == KEYUP) or not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
           return
        left = False
        right = False
        #KEYDOWN events toggle movement on
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
        #KEYUP events toggles movement off
        if event.type == KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
        #If left XOR right
        if left != right:
            if left:
                game_object.acc_direction = -1
            if right:
                game_object.acc_direction = 1
        #Slow character down when there's conflicting input or no input
        else:
            game_object.acc_direction = 0

    def y_movement(self, event, game_object):
        """
        used to update the v velocity of the object
        """
        #KEYUP events toggles movement off
        if event.type == KEYDOWN:
            if event.key == pygame.K_UP and game_object.jumps > 0:
                game_object.vel_y = game_object.jump_vel
                game_object.jumps -= 1
                print("up", game_object.vel_y)

    def update_motion(self):
        """
        Updates the position and velocity of each character.
        """
        for char in self.characters:
            if char.in_air(800 - 1.5 * char.height):
                char.vel_y += self.g
            elif char.vel_y  > 0:
                char.vel_y = 0
                char.pos_y = 800 - char.height
                char.jumps = char.max_jumps
            char.accelerate()
            char.move()

    def quit(self, event):
        if event.type == QUIT:
            self.game_running = False
