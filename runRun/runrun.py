import os, sys
import pygame
from pygame.locals import *
from helpers import *
import random
import math

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


BLUE = (0,0,255)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def main(SCREEN_WIDTH, SCREEN_HEIGHT):

    """Initialize PyGame"""
    pygame.init()
    time = pygame.time.Clock()

    pygame.font.init()

    """Set the window Size"""

    """Create the Screen"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    """Create the background"""
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    player = Player()
    ground = Ground()
    # items = Items(ground)
    coin = Coin()

    active_sprite_list = pygame.sprite.Group()

    player.rect.x = 0
    player.rect.y = .5 * SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    spritesgroups = pygame.sprite.Group()
    coin.rect.x =  SCREEN_WIDTH
    coin.rect.y = .3 * SCREEN_HEIGHT
    spritesgroups.add(coin)


    """This is the Main Loop of the Game"""

    # """Load All of our Sprites"""
    # self.LoadSprites()

    # """Create the background"""
    #     self.background = pygame.Surface(self.screen.get_size())
    #     self.background = self.background.convert()
    #     self.background.fill((0,0,0))

    #pygame.key.set_repeat(0, 30)

    while True:
        """Keep track of time"""
        time.tick(60)
        frame_time = time.get_time()

        """Check for player inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    player.jump(ground_height)
                if event.key == pygame.K_LEFT:
                    player.move_left(frame_time)
                elif event.key == pygame.K_RIGHT:
                    player.move_right(frame_time)
            elif player.change_x != 0:
                player.stop(frame_time)

        """Check for collisions with rocks and end game """

        """Check for collision with coins and update score"""
        lstCols = pygame.sprite.spritecollide(player, spritesgroups, True)
        player.coins = player.coins + len(lstCols)

        """Advance the ground"""
        ground_height = ground.advance(frame_time, player.rect.x, player.rect.width) #items
        ground.build() #items

        player.update(frame_time, ground_height)
        coin.update(ground_height)

        """Draw the game"""
        #
        # screen.blit(background, (0, 0))
        # if pygame.font:
        #     font = pygame.font.Font(None, 36)
        #     text = font.render("Coins: %s" % player.coins, 1, (255, 0, 0))
        #     textpos = text.get_rect(centerx= SCREEN_WIDTH/2, centery = 50)
        #     screen.blit(text, textpos)


        screen.blit(background, (0, 0))
        active_sprite_list.draw(screen)
        spritesgroups.draw(screen)
        ground.draw(screen, GREEN)
        pygame.display.flip()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.image.load('data/images/snake.png'))
        self.rect = self.image.get_rect()
        self.acceleration_y = .01
        self.acceleration_x = .02
        self.jump_power = 1.5
        self.speed_limit = 4
        self.change_x = 0
        self.change_y = 0
        self.coins = 0

    def update(self, t, ground_height):
        self.calc_grav(t, ground_height)

        self.rect.y += self.change_y * t
        self.rect.x += self.change_x * t

        if self.rect.x < 0:
            self.rect.x = 0
            self.change_x = 0
        elif self.rect.x + self.rect.width > SCREEN_WIDTH/1.2:
            self.rect.x = SCREEN_WIDTH/1.2 - self.rect.width
            self.change_x = 0

    def calc_grav(self, t, ground_height):
        bottom = self.rect.y + self.rect.height
        if bottom < ground_height:
            self.change_y += self.acceleration_y * t

        if bottom >= ground_height - 5 and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = ground_height - self.rect.height

    def jump(self, height):
        bottom = self.rect.y + self.rect.height
        threshold = height - 10
        if bottom > threshold:
            self.change_y = -self.jump_power

    def move_right(self, t):
        self.change_x += self.acceleration_x * t
        if self.change_x > self.speed_limit:
            self.change_x = self.speed_limit

    def move_left(self, t):
         self.change_x -= self.acceleration_x * t
         if self.change_x < -self.speed_limit:
             self.change_x = -self.speed_limit

    def stop(self, t):
        self.change_x = 0


# class Item(pygame.sprite.Sprite):
#     """ Class representing an item the player can interact with"""
#     def __init__(self):
#         super().__init__()


class Coin(pygame.sprite.Sprite): #Item
    """ Class representing a coin"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Item.__init__()
        super().__init__()
        self.image = (pygame.image.load('data/images/coin.png'))
        self.rect = self.image.get_rect()
        self.change_x = -5
        self.change_y = 6

    def update(self, ground_height):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.y + self.rect.height >= ground_height:
            self.change_y = -6
        elif self.rect.y <= 0:
            self.change_y = 6

class Ground():
    """ Class representing the ground """
    def __init__(self):
        self.speed = 1
        self.ground_min = .9 * SCREEN_HEIGHT
        self.ground_max = .4 * SCREEN_HEIGHT
        self.ground_height = [.75 * SCREEN_HEIGHT] * (2 * SCREEN_WIDTH)

    def advance(self, t, start, end): #items
        height = min(self.ground_height[start:start+end])
        distance = t * self.speed
        del self.ground_height[:distance]
        # items.advance(distance)
        return height

    def draw(self, screen, color):
        for x in range(1, SCREEN_WIDTH):
            y = int(self.ground_height[x-1])
            pygame.draw.line(screen, color, (x, y), (x, y+5))

    def build(self, score = 0): #items
        if len(self.ground_height) > 1.1 * SCREEN_WIDTH:
            return

        pick = random.randint(1,10)
        if pick > 7:
            self.slope() #items
        else:
            self.flat() #items

    def slope(self): #items
        start = self.ground_height[-1]
        space_below = self.ground_min - start
        space_above = self.ground_max - start

        rise = random.randint(space_above, space_below)
        run = random.randint(abs(rise) * 2, SCREEN_WIDTH)
        slope = rise/ run

        for x in range(run):
            y = int(slope * x) + start
            self.ground_height.append(y)

        # items.add(run)

    def flat(self): #items
        length = random.randint(20, SCREEN_WIDTH)
        height = self.ground_height[-1]
        self.ground_height.extend([height] * length)

        # items.add(length)

# class Items():
#     """ Class representing a list all the items in the game"""
#
#     def __init__(self, ground):
#         self.item_list = ['None'] * len(ground.ground_height)
#         self.chance_coin = .01
#
#     def advance(self, distance):
#         for item in self.item_list[:distance]:
#             if item != 'None':
#                 item.kill
#         del self.item_list[:distance]
#         for item in self.item_list:
#             if item != 'None':
#                 item.location -= distance
#
#     def add(self, amount):
#         self.item_list.extend(['None'] * amount)





if __name__ == "__main__":
    # MainWindow = RunRunMain()
    # MainWindow.MainLoop()
    main(SCREEN_WIDTH, SCREEN_HEIGHT)
