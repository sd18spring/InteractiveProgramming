import pygame
class Character:
    def __init__(self, pos_x = 0, pos_y = 0, label = "blank",
                     attack = 10,
                     defense = 10,
                     weight = 10,
                     jump_vel = -100,
                     acceleration = 3,
                     speed = 15,
                     width = 75,
                     height = 150,
                     max_health = 100,
                     max_jumps = 3, keys = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up" : pygame.K_UP, "down": pygame.K_DOWN, "attack": pygame.K_SLASH}):
        self.keys = keys
        self.label = label
        self.attack = attack
        self.defense = defense
        self.weight = weight
        self.jump_vel = jump_vel
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.health = max_health
        self.left = True
        self.right = False
        self.attacking = False
        self.damaged = False
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = acceleration
        self.speed = speed
        self.acc_direction = 0
        self.lives = 3
        self.max_jumps = max_jumps
        self.jumps = max_jumps
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.attack_rect = pygame.Rect(self.pos_x, self.pos_y, 0, 0)
        self.attack_time = 0

    def __str__(self):
        output = self.label + ':\n'
        output += "attack: " + str(self.attack)
        output += "\ndefense: " + str(self.defense)
        output += "\nweight: " + str(self.weight)
        output += "\njump vel: " + str(self.jump_vel)
        output += "\nacceleration: " + str(self.acc_x)
        output += "\nspeed: " + str(self.speed)
        output += "\nwidth: " + str(self.width)
        output += "\nheight: " + str(self.height)
        output += "\nhealth: " + str(self.health)
        return output

    def in_air(self, terrain):
        """
        checks to see if character is in the air, or supported by terrain
        *args are (probably) terrain objects and their coordinates
        """
        if self.pos_y >= terrain:
            return False
        return True

    def alive(self):
        """
        checks to see if the character is still alive
        """
        return self.health > 0

    def accelerate(self):
        """
        updates the acceleration of the character, for movement on each frame
        when there is no movement, acceleration = 0
        direction is -1 or 1
        """
        self.vel_x += self.acc_x * self.acc_direction
        if self.vel_x > self.speed:
            self.vel_x = self.speed
        if self.vel_x < -self.speed:
            self.vel_x = -self.speed

        #Decelerates the object when there are no inputs.
        # if self.vel_x > 0:
        #     self.vel_x -= self.acc_x
        # elif self.vel_x < 0:
        #     self.vel_x += self.acc_x

    def move(self):
        """
        updates the position of the character laterally.
        direction is either -1 or 1
        """
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def attack_action(self):
        """
        updates the hitbox of the character to reflect the action of an attack.
        """
        #If the attacking time is up, then toggle off attacking.
        if self.attack_time < 1:
            self.attack_time = 0
            self.attacking = False

        if self.attacking:
            #offsets that represent the size of the attack hitbox
            x_offset = self.width * 0.7
            y_offset = self.height * 0.5
            self.vel_x = 0
            #If the character is facing left, draw the attack hitbox on the left
            if self.left:
                self.attack_rect = pygame.Rect(self.pos_x - x_offset,
                                               self.pos_y + y_offset,
                                               x_offset,
                                               y_offset)
            #If char is facing right, draw the attack hitbox on the right
            else:
                self.attack_rect = pygame.Rect(self.pos_x + self.width,
                                               self.pos_y + y_offset,
                                               x_offset,
                                               y_offset)
            #update the time spent attacking
            self.attack_time -= 1
        #If the character isn't attacking, remove the attack hitbox
        else:
            self.attack_rect = pygame.Rect(self.pos_x, self.pos_y, 0, 0)
