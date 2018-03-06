class Character:
    def __init__(self, label
                     attack = 10,
                     defense = 10,
                     weight = 10,
                     jump_vel = 10,
                     speed = 10,
                     pos_x = 0,
                     pos_y = 0,
                     width = 10
                     height = 25
                     max_health = 100):
        self.label = label
        self.attack = attack
        self.defense = defense
        self.weight = weight
        self.jump_vel = jump_vel
        self.speed = speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.health = max_health
        self.vel_y = 0


        self.lives = 3

    def __str__(self):
        output = self.label + ':\n'
        output += "attack: " + str(self.attack)
        output += "\ndefense: " + str(self.defense)
        output += "\nweight: " + str(self.weight)
        output += "\njump vel: " + str(self.jump_vel)
        output += "\nspeed: " + str(self.speed)
        output += "\nwidth: " + str(self.width)
        output += "\nheight: " + str(self.height)
        output += "\nhealth: " + str(self.health)
        return output

    def in_air(self, *args):
        """
        checks to see if character is in the air, or supported by terrain
        *args are (probably) terrain objects and their coordinates
        """
        for pos_y in args:
            if self.pos_y == pos_y and self.:
                return False
        return True

    def alive(self):
        """
        checks to see if the character is still alive
        """
        return self.health > 0

    def move(self, direction):
        """
        updates the position of the character laterally.
        direction is either -1 or 1
        """
        if self.pos_x += direction * self.speed
