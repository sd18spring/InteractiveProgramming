import pygame
import constants
import pyautogui

class SpriteSheet(object):
    """Class used to grab images out of a sprite sheet"""

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """Grab image out of a sprite sheet.
        x,y: x,y location of sprite
        width, height: width/height of sprite"""

        #create new blank image
        image = pygame.Surface([width, height]).convert()

        #copy the sprite from large sheet onto small image
        image.blit(self.sprite_sheet, (0,0), (x,y, width, height))

        #assuming black works as the transparent color
        image.set_colorkey(constants.WHITE)

        #Return the image
        return image

class Cloud(pygame.sprite.Sprite):
    """Takes two arguments and generates a cloud
    sprite_sheet_data: an array of 4 numbers (xpos, ypos, width, height) of a sprite from the sprite sheet
    sheet_name: a string of the filename that the sprite is being pulled from"""
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__()

        sprite_sheet = SpriteSheet(sheet_name)
        self.image = sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], sprite_sheet_data[2], sprite_sheet_data[3])

        self.rect = self.image.get_rect()

class MovingCloud(Cloud):
    """Creates a moving cloud"""
    def __init__(self, sprite_sheet_data, sheet_name):
        super().__init__(sprite_sheet_data, sheet_name)

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        def update(self):
            """Move the cloud"""
            #move left/right
            self.rect.x += self.change_x

            #move up/down
            self.rect.y += self.change_y

class Scene():
    """Generic super class used to define the objects, can create subclasses to actually create specific landscapes"""
    def __init__(self):
        #Lists of all sprites needed for scenery
        self.cloud_list = None
        self.star_list = None

        #background image
        self.background = pygame.image.load("summerbackground.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.background_size = self.background.get_size()
        self.background_rect = self.background.get_rect()
        self.w, self.h = self.background_size
        self.x = 0
        self.x1 = self.w

        #store original locations of sprites
        self.blkoriginal = []
        self.purporiginal = []
        self.smalloriginal = []

        #How far this world has been scrolled left/right
        self.world_shift = 0
        self.smallcloud_list = pygame.sprite.Group()
        self.purpcloud_list = pygame.sprite.Group()
        self.blkcloud_list = pygame.sprite.Group()
        self.star_list = pygame.sprite.Group()
        self.balloon_list = pygame.sprite.Group()

    #Update everything on this level
    def update(self):
        self.smallcloud_list.update()
        self.purpcloud_list.update()
        self.blkcloud_list.update()
        #self.cactus_list.update()
        #self.balloon_list.update()
        #self.star_list.update()

    #Update everything in the landscapes
    def draw(self, screen):

        #Draw all the sprite lists we have
        self.blkcloud_list.draw(screen)
        self.purpcloud_list.draw(screen)
        self.smallcloud_list.draw(screen)
        #self.star_list.draw(screen)

    def shift_world(self, shift_x, screen):
        #make everything scroll at a nice, constant rate

        #keep track of the shift amount
        self.world_shift += shift_x

        #Keep track of background loop shift
        self.x += shift_x
        self.x1 += shift_x
        screen.blit(self.background, (self.x,0))
        screen.blit(self.background, (self.x1,0))
        if self.x < -self.w:
            self.x = self.w
        if self.x1 < -self.w:
            self.x1 = self.w

        count = 0
        #Go through all the sprite lists and shift
        for smallcloud in self.smallcloud_list:
            smallcloud.rect.x += shift_x - 5
            if smallcloud.rect.x >= 1920:
                smallcloud.rect.x = self.smalloriginal[count]
            count+=1

        for purpcloud in self.purpcloud_list:
            purpcloud.rect.x += shift_x -3

        for blkcloud in self.blkcloud_list:
            blkcloud.rect.x += shift_x -1

        for star in self.star_list:
            star.rect.x += shift_x

class Summer(Scene):
    """Defintion for Fantasy live background"""

    def __init__(self, player):
        #Call parent constructor
        Scene.__init__(self)

        #Array with type of cloud, and x, y location of the cloud
        enviro = constants.summer

        #Go through the array above and add cloud_list
        for i in range(len(enviro)):
            if 0 <= i <= 3:
                block = Cloud(enviro[i][0], "blackclouds.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.blkoriginal.append(block.rect.x)
                self.blkcloud_list.add(block)
            elif 4 <= i <= 7:
                block = Cloud(enviro[i][0], "purpleclouds.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.purporiginal.append(block.rect.x)
                self.purpcloud_list.add(block)
            elif 8 <= i <= 11:
                block = Cloud(enviro[i][0], "smallclouds.png")
                block.rect.x = enviro[i][1]
                block.rect.y = enviro[i][2]
                self.smalloriginal.append(block.rect.x)
                self.smallcloud_list.add(block)
            #elif i == 12:
                #self.cactus =

class Player():
    def __init__(self):
        self.x, self.y = pyautogui.position()

    def click(self):
        """Updates the location of the cursor"""
        self.x, self.y = pyautogui.position()
#needs to generate sprites with a specific flow of animations when mouse is clicked
