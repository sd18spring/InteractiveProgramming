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
    """Set the window Size"""

    """Create the Screen"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    """Create the background"""
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    player = Player()
    ground = Ground()
    # level_list = []
    # level_list.append(Level_01(player))

    # current_level_no = 0
    # current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    # player.level = current_level

    player.rect.x = 0
    player.rect.y = .5 * SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)


    """This is the Main Loop of the Game"""

    # """Load All of our Sprites"""
    # self.LoadSprites()

    # """Create the background"""
    #     self.background = pygame.Surface(self.screen.get_size())
    #     self.background = self.background.convert()
    #     self.background.fill((0,0,0))

    pygame.key.set_repeat(500, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    player.jump(ground_height)
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()

        """Check for collisions with rocks and end game """

        """Check for collision with coins and update score"""

        """Advance the ground"""
        ground_height = ground.advance()
        ground.build()

        player.update(ground_height)
        # current_level.update()


        """Draw the game"""
        # current_level.draw(screen)
        screen.blit(background, (0, 0))
        active_sprite_list.draw(screen)
        ground.draw(screen, GREEN)
        pygame.display.flip()


class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        self.image = (pygame.image.load('data/images/snake.png'))
        self.rect = self.image.get_rect()

        self.change_y = 0
        self.change_x = 0

        self.level = None

    def update(self, ground_height):
        self.calc_grav(ground_height)

        self.rect.y += self.change_y
        self.rect.x += self.change_x

    def calc_grav(self, ground_height):
        bottom = self.rect.y + self.rect.height
        if bottom < ground_height:
            self.change_y += 1

        if bottom >= ground_height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = ground_height - self.rect.height

    def jump(self, height):
        bottom = self.rect.y + self.rect.height
        threshold = height - 5
        if bottom > threshold:
            self.change_y = -15

    def move_right(self):
        self.change_x += .5

    def move_left(self):
        self.change_x -= -.5


class Coin(pygame.sprite.Sprite):
    pass
        # self.vSpeed = 4
        # self.maxVspeed = 4

class Ground():
    """ Class representing the ground """

    def __init__(self):
        self.speed = 10
        self.ground_min = .9 * SCREEN_HEIGHT
        self.ground_max = .4 * SCREEN_HEIGHT
        self.ground_height = [.75 * SCREEN_HEIGHT] * (2 * SCREEN_WIDTH)

    def advance(self, x = 0):
        height = self.ground_height[x]
        del self.ground_height[:self.speed]
        return height

    def draw(self, screen, color):
        for x in range(1, SCREEN_WIDTH):
            y = int(self.ground_height[x-1])
            pygame.draw.line(screen, color, (x, y), (x, y+5))

    def build(self, score = 0):
        if len(self.ground_height) > 1.1 * SCREEN_WIDTH:
            return

        pick = random.randint(1,10)
        if pick > 7:
            self.slope()
        else:
            self.flat()

    def slope(self):
        start = self.ground_height[-1]
        space_below = self.ground_min - start
        space_above = self.ground_max - start

        rise = random.randint(space_above, space_below)
        run = random.randint(abs(rise) * 2, SCREEN_WIDTH)
        slope = rise/ run

        for x in range(run):
            y = int(slope * x) + start
            self.ground_height.append(y)

    def flat(self):
        length = random.randint(20, SCREEN_WIDTH)
        height = self.ground_height[-1]
        self.ground_height.extend([height] * length)




if __name__ == "__main__":
    # MainWindow = RunRunMain()
    # MainWindow.MainLoop()
    main(SCREEN_WIDTH, SCREEN_HEIGHT)
