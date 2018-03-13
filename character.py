import pygame
class Character:
    def __init__(self, pos_x = 300, pos_y = 0, label = "blank",
                     attack = 10,
                     defense = 10,
                     weight = 10,
                     jump_vel = -80,
                     acceleration = 3,
                     speed = 15,
                     width = 75,
                     height = 150,
                     max_health = 100,
                     max_jumps = 3, keys = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up" : pygame.K_UP, "down": pygame.K_DOWN, "attack": pygame.K_SLASH},
                     left_img = "left.png",
                     right_img = "right.png",
                     up_img = "up.png",
                     down_img = "down.png",
                     lives = 3,
                     player = 1):
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
        self.left = False
        self.right = False
        self.attacking = False
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = acceleration
        self.speed = speed
        self.acc_direction = 1
        self.lives = 3
        self.max_jumps = max_jumps
        self.jumps = max_jumps
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.attack_rect = pygame.Rect(self.pos_x, self.pos_y, 0, 0)
        self.attack_time = 0
        self.damage_time = 0
        self.keys = keys
        self.left_img = pygame.transform.scale(pygame.image.load(left_img), (self.width, self.height))
        self.right_img = pygame.transform.scale(pygame.image.load(right_img), (self.width, self.height))
        self.up_img = pygame.transform.scale(pygame.image.load(up_img), (self.width, self.height))
        self.down_img = pygame.transform.scale(pygame.image.load(down_img), (self.width, self.height))
        self.player = player



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
        return not self.rect.colliderect(terrain)

    def alive(self):
        """
        checks to see if the character is still alive
        """
        return self.health > 0

    def accelerate(self):
        """
        when there is no movement, acceleration = 0
        direction is -1 or 1
        """
        #self.vel_x += self.acc_x * self.acc_direction
        #if self.vel_x > self.speed:
        #    self.vel_x = self.speed
        #if self.vel_x < -self.speed:
        #    self.vel_x = -self.speed

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
        #For the second to last frame of the damaged animation, the velocity
        #should be set to zero
        if self.damage_time == 1:
            self.vel_x = 0
            self.vel_y = 0
        if self.damage_time > 0:
            self.damage_time -= 1

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        if(self.pos_y > 1000):
            self.pos_y = 0
            self.pos_x = 500
            self.lives -= 1

    def attack_action(self):
        """
        updates the hitbox of the character to reflect the action of an attack.
        """
        if self.damage_time > 0:

            self.attack_time = 0
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
                self.right = True
                self.attack_rect = pygame.Rect(self.pos_x + self.width,
                                               self.pos_y + y_offset,
                                               x_offset,
                                               y_offset)
            #update the time spent attacking
            self.attack_time -= 1
        #If the character isn't attacking, remove the attack hitbox
        else:
            #put the hitbox underground where it can't interfere wither others
            self.attack_rect = pygame.Rect(self.pos_x, 1000, 0, 0)

    def detect_damage(self, attack_hitbox, direction):
        """
        detects whether a character object is subjected to an attack or not, and
        then appropriately designates a knockback force.
        """
        if self.rect.colliderect(attack_hitbox):
            #add 10 to the damage timer
            self.damage_time = 10
            #set push directions
            self.vel_x = direction * self.speed * 2.5 #I changed these from 1.5 to 2.5 to be more dramatic, feel free to change back
            self.vel_y = -abs(self.vel_x * 2.5)
