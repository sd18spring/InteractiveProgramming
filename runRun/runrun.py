import os, sys
import pygame
from pygame.locals import *
from helpers import *

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

    player = Player()
    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 0
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    """This is the Main Loop of the Game"""

    # """Load All of our Sprites"""
    # self.LoadSprites()

    # """Create the background"""
    #     self.background = pygame.Surface(self.screen.get_size())
    #     self.background = self.background.convert()
    #     self.background.fill((0,0,0))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        active_sprite_list.update()
        current_level.update()

        current_level.draw(screen)
        active_sprite_list.draw(screen)
            #
            # self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    pygame.quit()


class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = (pygame.image.load('runningman.png'))
        self.rect = self.image.get_rect()

        self.change_y = 0

        self.level = None

    def update(self):
        self.calc_grav()

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top

        self.rect.y += self.change_y

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.15

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

class Level(object):

    def __init__(self,player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):

        screen.fill(BLUE)

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

class Level_01(Level):

    def __init__(self, player):

        Level.__init__(self, player)

        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Coin(pygame.sprite.Sprite):
    pass
        # self.vSpeed = 4
        # self.maxVspeed = 4

class Platform(pygame.sprite.Sprite):
    """ Temporary for platforms"""

    def __init__(self, w, h):
        super().__init__()

        self.image = pygame.Surface([w,h])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()


if __name__ == "__main__":
    # MainWindow = RunRunMain()
    # MainWindow.MainLoop()
    main(SCREEN_WIDTH, SCREEN_HEIGHT)
