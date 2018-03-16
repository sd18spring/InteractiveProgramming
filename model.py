import character
import terrain
import random
import pygame
from pygame.locals import *

class Model:
    def __init__(self, *args):
        self.game_running = True
        self.game_over = False
        self.g = 15
        self.terrains = []
        self.characters = []

        for char in args:
            self.characters.append(char)

        self.terrains.append(terrain.Terrain((200,600), (1100,50)))

    def x_movement(self, event, game_object):
        """
        Toggles the different modes of acceleration depending on key up
        events and key down events.
        """
        if (not (event.type == KEYDOWN or event.type == KEYUP) or
           game_object.attacking or
           game_object.damage_time > 0 or
           game_object.shielding):
           return

        #KEYDOWN events toggle movement on
        if event.type == KEYDOWN:
            if event.key == game_object.keys["left"]:
                game_object.left = True
                game_object.right = False
                game_object.vel_x = -game_object.speed
            elif event.key == game_object.keys["right"]:
                game_object.right = True
                game_object.left = False
                game_object.vel_x = game_object.speed
        #KEYUP events toggles movement off
        if event.type == KEYUP:
            if (event.key == game_object.keys["left"] and
               not game_object.right):
                game_object.vel_x = 0
            elif (event.key == game_object.keys["right"] and
                 not game_object.left):
                game_object.vel_x = 0

        """
        #If left XOR right
        if game_object.left != game_object.right:
            if game_object.left:
                game_object.vel_x = -game_object.speed
            if game_object.right:
                game_object.vel_x = game_object.speed
        #Slow character down when there's conflicting input or no input
        else:
            game_object.vel_x = 0
        """
    def y_movement(self, event, game_object):
        """
        used to update the v velocity of the object
        """
        if event.type == KEYDOWN:
            if event.key == game_object.keys["up"] and game_object.jumps > 0:
                game_object.vel_y = game_object.jump_vel
                game_object.jumps -= 1

    def shield(self,event, game_object):
        """
        Used to update the shield state of a character
        """
        if (game_object.attack_time > 0 or
           game_object.damage_time > 0):
           return
        if event.type == KEYDOWN:
            if event.key == game_object.keys["down"]:
                game_object.shielding = True
        if event.type == KEYUP:
            if event.key == game_object.keys["down"]:
                game_object.shielding = False

    def attack_command(self, event, game_object):
        """
        Used to toggle the attacking mode for a character object for a given
        amount of time.
        """
        if game_object.shielding:
            return
        if event.type == KEYDOWN:
            #NOTE: Change to custom/dynamic character attack button.
            if event.key == game_object.keys["attack"]:
                game_object.attacking = True
                #number of frames spent attacking
                game_object.attack_time = 30

    def update_motion(self):
        """
        Updates the position and velocity and attack hitbox of each character.
        """
        for char in self.characters:
            if char.in_air(self.terrains[0].rect):
                char.vel_y += self.g
            elif char.vel_y  > 0:
                char.vel_y = 0
                char.pos_y = self.terrains[0].rect.top - char.height + 1
                char.jumps = char.max_jumps
            for other_chars in self.characters:
                if other_chars.left:
                    char.detect_damage(other_chars, -1)
                else:
                    char.detect_damage(other_chars, 1)
            print(char.damage_time)

            char.move()
            char.attack_action()

    def check_lives(self):
        """
        Checks to see a player has lost
        """
        for char in self.characters:
            if char.lives < 1:
                self.game_over = True

    def quit(self, event):
        if event.type == QUIT:
            self.game_running = False
