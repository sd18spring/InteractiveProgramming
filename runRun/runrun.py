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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main(SCREEN_WIDTH, SCREEN_HEIGHT):
    """Initialize PyGame"""
    pygame.init()
    time = pygame.time.Clock()
    coin_time_past = 0
    rock_time_past = 0
    bird_time_past = 0

    pygame.font.init()
    font = pygame.font.Font(None, 36)

    """Create the Screen"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    """Create the background"""
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    """Initialize Ground, Player, and Items """
    ground = Ground()

    player = Player()
    player_list = pygame.sprite.Group()
    player_list.add(player)

    coins_group = pygame.sprite.Group()
    coin = Coin()
    coins_group.add(coin)

    rocks_group = pygame.sprite.Group()
    rock = Rock()
    rocks_group.add(rock)

    bird_list = pygame.sprite.Group()
    bird = Bird()
    bird_list.add(bird)

    health = 10

    """This is the Main Loop of the Game"""
    #pygame.key.set_repeat(0, 30)

    Running = True
    while Running:
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


        """Check for collisions with rocks and update health"""
        lstCols2 = pygame.sprite.spritecollide(player, rocks_group, False)
        if len(lstCols2) > 0:
            player.deflect(frame_time)
            player.health = player.health - 1

        if player.health < 0:
            Running = False

        """Check for collision with coins and update score"""
        lstCols = pygame.sprite.spritecollide(player, coins_group, True)
        player.coins = player.coins + len(lstCols)

        """Check for collision with birds and update health"""
        lstCols3 = pygame.sprite.spritecollide(player, bird_list, False)
        if len(lstCols3) > 0:
            player.deflect(frame_time)
            player.health = player.health - 1

        """Advance the game"""
        ground_height = ground.advance(frame_time, player, coins_group, rocks_group, bird_list)
        ground_height_right = ground.ground_height[SCREEN_WIDTH]
        ground.build()

        if player.rect.y > ground_height:
            Running = False

        """Add new coins"""
        coin_time_past += frame_time
        if coin_time_past > 2000 and ground_height_right < SCREEN_HEIGHT:
            coin_time_past = 0
            coins_group.add(Coin(ground_height_right))

        """Add new rock (s) """
        num = random.randint(0, 400)
        if num == 2:
            rock_time_past = 0
            rocks_group.add(Rock(ground_height_right))

        """Add new bird"""
        bird_time_past += frame_time
        if bird_time_past > 2000 and ground_height_right < SCREEN_HEIGHT:
            bird_time_past = 0
            bird_list.add(Bird())

        """Update the player """
        player.update(frame_time, ground_height)

        """Draw the game"""
        screen.blit(background, (0, 0))
        text = font.render("Score: %s" % player.coins, 1, (255, 0, 0))
        textpos = text.get_rect(centerx= SCREEN_WIDTH/2, centery = 50)
        screen.blit(text, textpos)
        fps = font.render("FPS: %.2f" % time.get_fps(), 1, (255, 0, 0))
        fpspos = fps.get_rect(centerx= 80, centery = 50)
        htext = font.render("Health: %s" % player.health, 1, (255, 0, 0))
        hpos = htext.get_rect(centerx = 700, centery = 50)
        screen.blit(htext, hpos)
        screen.blit(fps, fpspos)
        player_list.draw(screen)
        coins_group.draw(screen)
        rocks_group.draw(screen)
        bird_list.draw(screen)
        ground.draw(screen, GREEN)
        pygame.display.flip()

    score = 0
    screen.blit(background, (0, 0))
    text1 = font.render("GAME OVER", 2, (255, 0, 0))
    text2 = font.render("Score: %s" % player.coins, 2, (255, 0, 0))
    text1pos = text1.get_rect(centerx= SCREEN_WIDTH/2, centery = SCREEN_HEIGHT/2)
    text2pos = text2.get_rect(centerx= SCREEN_WIDTH/2, centery = SCREEN_HEIGHT/2 + 50)
    screen.blit(text1, text1pos)
    screen.blit(text2, text2pos)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()



class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.image.load('data/images/runningman.png'))
        self.rect = self.image.get_rect()
        self.acceleration_y = .007
        self.acceleration_x = .02
        self.jump_power = 1.5
        self.speed_limit = 4
        self.change_x = 0
        self.change_y = 0
        self.coins = 0
        self.jumping =  0
        self.health = 10

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

    def deflect(self, t):
        self.rect.x += 25
        self.rect.y += 50


class Coin(pygame.sprite.Sprite):
    """ Class representing a coin"""
    def __init__(self, height = 0.75 * SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = (pygame.image.load('data/images/coin.png'))
        self.rect = self.image.get_rect()
        self.ground = height
        self.rect.y = self.ground - self.rect.height
        self.rect.x = SCREEN_WIDTH - self.rect.width
        self.change_y = 0
        self.y_speed = .1* (random.random() + 1)

    def update(self, t, distance):
        self.rect.x -= distance
        self.rect.y += self.change_y * t
        if self.rect.y + self.rect.height >= self.ground:
            self.change_y = -self.y_speed
        elif self.rect.y <= self.ground - self.rect.height - .25 * SCREEN_HEIGHT:
            self.change_y = self.y_speed

class Rock(pygame.sprite.Sprite):
    """ Class representing a rock"""
    def __init__(self, height = .75 * SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = (pygame.image.load('data/images/boulder.png'))
        self.rect = self.image.get_rect()
        self.rect.y = height- self.rect.height
        self.rect.x = SCREEN_WIDTH + self.rect.width
        self.ground = height

    def update(self, distance):
        self.rect.x -= distance

class Ground():
    """ Class representing the ground """
    def __init__(self):
        self.speed = .7
        self.ground_min = .9 * SCREEN_HEIGHT
        self.ground_max = .4 * SCREEN_HEIGHT
        self.ground_height = [.75 * SCREEN_HEIGHT] * (2 * SCREEN_WIDTH)

    def advance(self, t, player, coin_list, rock_list, bird_list):
        start = player.rect.x
        end = start + player.rect.width
        height = min(self.ground_height[start:end])
        distance = int(t * self.speed)
        del self.ground_height[:distance]
        [coin.update(t, distance) for coin in coin_list]
        [rock.update(distance) for rock in rock_list]
        [bird.update(distance) for bird in bird_list]
        return height

    def draw(self, screen, color):
        for x in range(1, SCREEN_WIDTH):
            y = int(self.ground_height[x-1])
            pygame.draw.line(screen, color, (x, y), (x, y+5))

    def build(self, score = 0):
        if len(self.ground_height) > 1.1 * SCREEN_WIDTH:
            return

        pick = random.random()
        if pick > .9:
            self.gap()
        elif pick > .6:
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
        length = random.randint(20, SCREEN_WIDTH/2)
        height = self.ground_height[-1]
        self.ground_height.extend([height] * length)

    def gap(self):
        length = 300
        height = self.ground_height[-1]
        self.ground_height.extend([SCREEN_HEIGHT] * length)
        self.ground_height.extend([height] * 100)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = (pygame.image.load('data/images/bird.png'))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width
        self.rect.y = 100
        self.bounce = -1
        self.change_height = 20

    def update(self, distance):
        self.rect.x -= distance

if __name__ == "__main__":
    # MainWindow = RunRunMain()
    # MainWindow.MainLoop()
    main(SCREEN_WIDTH, SCREEN_HEIGHT)
