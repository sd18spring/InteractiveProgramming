"""Interactive Programming Mini-Project 4: Live Wallpaper

Authors: Hwei-Shin Harriman and Jessie Potter
References: http://programarcadegames.com/python_examples/en/sprite_sheets/"""
import pygame
import constants
import random
import math

class SpriteSheet(object):
    """Class used to grab images out of a sprite sheet"""

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        """Grab image out of a sprite sheet.
        x,y: x,y location of sprite
        width, height: width/height of sprite"""

        #create new blank image
        image = pygame.Surface([width, height], pygame.SRCALPHA)

        #copy the sprite from large sheet onto small image
        image.blit(self.sprite_sheet, (0,0), (x,y, width, height))

        #Return the image
        return image

class Sprite(pygame.sprite.Sprite):
    """Takes two arguments and generates a sprite
    sprite_sheet_data: an array of 4 numbers (xpos, ypos, width, height) of a sprite from the sprite sheet
    sheet_name: a string of the filename that the sprite is being pulled from"""
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__()

        sprite_sheet = SpriteSheet(sheet_name)
        self.image = sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], sprite_sheet_data[2], sprite_sheet_data[3])

        self.rect = self.image.get_rect()
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, shift_x):
        return True

class Balloon(Sprite):
    """Takes two arguments and generates a balloon
    sprite_sheet_data: an array of 4 numbers (xpos, ypos, width, height) of a sprite from the sprite sheet
    sheet_name: a string of the filename that the sprite is being pulled from"""
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)
        self.change_x =0
        self.change_y = 1

        self.boundary_top = self.rect.y + 2
        self.boundary_bottom = self.rect.y - 2
        self.age = 0
        self.rate = random.randint(10,20)

    def update(self, shift_x):
        self.age += 1

        #move up/down
        self.rect.y = 2*math.sin(self.age/self.rate) + self.rect.y

        #move left/right
        self.rect.x += shift_x

        #survive until off-screen to the left
        return self.rect.x >= -200

class BlackCloud(Sprite):
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)

    def update(self, shift_x):
        #move left/right
        self.rect.x += shift_x - 1
        if self.rect.x < -2100:
            self.rect.x = random.randint(20,38)*100
        return True

class PurpleCloud(Sprite):
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)

    def update(self, shift_x):
        #move left/right
        self.rect.x += shift_x - 2
        if self.rect.x < -1500:
            self.rect.x = random.randint(20,38)*100
        return True

class SmallCloud(Sprite):
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)

    def update(self, shift_x):
        #move left/right
        self.rect.x += shift_x - 3
        if self.rect.x < -1000:
            self.rect.x = random.randint(20,38)*100
        return True

class Cactus(Sprite):
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)
    def update(self, shift_x):
        #move left/right
        self.rect.x += shift_x
        if self.rect.x < -1000:
            self.rect.x = 2958
        return True

class Flower(Sprite):
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)

    def update(self, shift_x):
        #move left/right
        self.rect.x += shift_x
        return self.rect.x >= -200

class Scene():
    """Generic super class used to define the objects, can create subclasses to actually create specific landscapes"""
    def __init__(self):

        #background image
        self.background = pygame.image.load("summerbackground.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.background_size = self.background.get_size()
        self.background_rect = self.background.get_rect()

        self.w, self.h = self.background_size
        self.x = 0
        self.x1 = self.w

        #How far this world has been scrolled left/right
        self.world_shift = 0

        #marker rectangle object for flower
        self.flox = 2971
        self.active_sprites = []

    #Update everything on this level
    def update(self, shift_x):

        sprites = self.active_sprites
        self.active_sprites = []
        for s in sprites:
            survive = s.update(shift_x)
            if survive:
                self.active_sprites.append(s)

    #Update everything in the landscapes
    def draw(self, screen):
        for s in self.active_sprites:
            s.draw(screen)

    def shift_world(self, shift_x, screen):
        #make everything scroll at a nice, constant rate

        #keep track of the shift amount
        self.world_shift += shift_x

        #Keep track of background loop shift
        self.x += shift_x
        self.x1 += shift_x
        self.flox += shift_x
        screen.blit(self.background, (self.x,0))
        screen.blit(self.background, (self.x1,0))
        if self.x < -self.w:
            self.x = self.w
        if self.x1 < -self.w:
            self.x1 = self.w
        if self.flox < -self.w+2971:
            self.flox = 2971

    def spawnballoon(self, xpos, ypos):
        currentballoon = constants.balloons[random.randint(0,10)]

        block = Balloon(currentballoon, "hotairballoons.png")
        block.rect.x = xpos
        block.rect.y = ypos
        self.active_sprites.append(block)

    def spawnflower(self, xpos, ypos):
        block = Flower(constants.FLOWER, "flower.png")
        block.rect.x = xpos
        block.rect.y = ypos
        self.active_sprites.append(block)

class Summer(Scene):
    """Defintion for Summer live background"""

    def __init__(self):
        #Call parent constructor
        Scene.__init__(self)

        #Array with type of cloud, and x, y location of the cloud
        enviro = constants.summer

        #Go through the array above and add cloud_list
        for i in range(len(enviro)):
            if 0 <= i <= 3:
                block = BlackCloud(enviro[i][0], "blackclouds.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.active_sprites.append(block)
            elif 4 <= i <= 7:
                block = PurpleCloud(enviro[i][0], "purpleclouds.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.active_sprites.append(block)
            elif 8 <= i <= 11:
                block = SmallCloud(enviro[i][0], "smallclouds.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.active_sprites.append(block)
            elif i == 12:
                block = Cactus(enviro[i][0], "bigcactus.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.active_sprites.append(block)
