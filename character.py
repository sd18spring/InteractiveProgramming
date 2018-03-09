class Character:
    def __init__(self, pos_x = 0, pos_y = 0, label = "blank",
                     attack = 10,
                     defense = 10,
                     weight = 10,
                     jump_vel = 10,
                     acceleration = .1,
                     width = 100,
                     height = 200,
                     max_health = 100):
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
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = acceleration
        self.lives = 3

    def __str__(self):
        output = self.label + ':\n'
        output += "attack: " + str(self.attack)
        output += "\ndefense: " + str(self.defense)
        output += "\nweight: " + str(self.weight)
        output += "\njump vel: " + str(self.jump_vel)
        output += "\nspeed: " + str(self.acc_x)
        output += "\nwidth: " + str(self.width)
        output += "\nheight: " + str(self.height)
        output += "\nhealth: " + str(self.health)
        return output

    def in_air(self, *args):
        """
        checks to see if character is in the air, or supported by terrain
        *args are (probably) terrain objects and their coordinates
        """
        #for pos_y in args:
            #if self.pos_y == pos_y and self.:
                #return False
        #return True

    def alive(self):
        """
        checks to see if the character is still alive
        """
        return self.health > 0

    def accelerate(self, direction):
        """
        updates the acceleration of the character, for movement on each frame
        when there is no movement, acceleration = 0
        direction is -1 or 1
        """
        print("ha")
        self.vel_x += self.acc_x * direction
        if self.vel_x > 5:
            self.vel_x = 5
        if self.vel_x < -5:
            self.vel_x = -5
    def move(self):
        """
        updates the position of the character laterally.
        direction is either -1 or 1
        """
        self.pos_x += self.vel_x
