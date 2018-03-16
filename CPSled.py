#THIS FILE IS DOPE
import pygame
from pygame.locals import *
import time
from random import *
clock = pygame.time.Clock()
"""
THINGS TO DO:
1. figure out how to generalize obstacle class w/ images #done
    a. add slow down and speed up functions #done
    b. figure out how logs will work
2. figure out how to generate more Obstacles
    a. create random tracks... if possible #yes!
3. Collisions
    a. somehow display that penguino has crashed #done
4. Extensions
    a. 2 player
    b. easy, medium, hard mode (single player)
    x. rotate screen
"""
class Penguin(pygame.sprite.Sprite): # code is from pygame documentation
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color
        self.image = pygame.image.load("penguin_smol.png")
        self.rect = self.image.get_rect()
    def moveUp(self, pixels):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y -= pixels

    def moveDown(self, pixels):
        if self.rect.y >= 340:
            self.rect.y = 340
        else:
            self.rect.y += pixels


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, image_name, rect = None):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect

    def moveLeft(self, pixels = 5):
        self.rect.x -= pixels
    def slowDown(self, pixels = 1):
        self.rect.x -= pixels
    def speedUp(self, pixels = 7):
        self.rect.x -= pixels

class Powerups(Obstacles):
    def speedUp(self, pixels = 7):
        self.rect.x -= pixels

class FinishLine(Obstacles):
    pass

class Sled_Main:
    def __init__(self):
        pygame.init()
        #track length is 4000 x 400
        size = (500, 400) #viewing frame is 500 x 400 pixels
        self.WHITE = pygame.Color(255, 255, 255)
        self.screen = pygame.display.set_mode(size)

    def loadSprites(self):
        self.penguin = Penguin()
    #    self.penguin.image = pygame.transform.rotate(self.penguin.image, -30)
        self.all_penguins = pygame.sprite.RenderPlain(self.penguin)
        self.boulders = pygame.sprite.RenderPlain()
        self.ice_patches = pygame.sprite.RenderPlain()
        self.finish_line_group = pygame.sprite.RenderPlain()
        for num_boulders in range(20):
            x_position = (num_boulders+1) * 400 #randint(260, 360)
            y_boulders = randint(1,3)
            for i in range(y_boulders):
                y_position = randrange(0, 340, 70)
                self.boulder = Obstacles("croproc.png", pygame.Rect(x_position, y_position, 50, 50))
                #self.boulder.rect = self.boulder.rect.move(35,105)
                #self.boulder.rect.inflate_ip(0, -10)
                #self.boulder.rect.inflate_ip(-20, -10)
                self.boulders.add(self.boulder)

        for num_ice_patches in range(8):
            x_position = (num_ice_patches+1) * 560 #randint(260, 360)
            y_position = randint(0, 340)
            self.ice_patch = Powerups("ice_patch_flat.png", pygame.Rect(x_position, y_position, 280, 70))
            self.ice_patches.add(self.ice_patch)

        self.finish_line = FinishLine("finish_line.png", pygame.Rect(1000, -2, 144, 404))
        self.finish_line_group.add(self.finish_line)

    def main_loop(self):
        self.loadSprites()
        list_of_obstacles = self.boulders.sprites()
        list_of_obstacles.extend(self.ice_patches.sprites())
        list_of_obstacles.append(self.finish_line)
        #pygame.font()
        font = pygame.font.Font(None, 32)

        running = True
        pygame.display.set_caption("Club Penguing Sledding Game")
        while running:

            current_time = str(pygame.time.get_ticks()/1000)
            timer = font.render(current_time, True, (0,0,0))

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()

            if self.penguin.rect.left > self.finish_line.rect.left+120:
                break

            hit = False
            ice = False
            finish = False
            for obstacle in list_of_obstacles:
                if self.penguin.rect.colliderect(obstacle.rect):
                    #print(self.penguin.rect.left)
                    #print(obstacle.rect.left)
                    hit = True
                    if type(obstacle) == Powerups:
                        ice = True
                    elif type(obstacle) == FinishLine:
                        finish = True
            for obstacle in list_of_obstacles:
                if ice or finish:
                    obstacle.speedUp()
                elif hit:
                    obstacle.slowDown()
                else:
                    obstacle.moveLeft()
            if hit and not ice and not finish:
                self.penguin.image = pygame.image.load("fallen_penguin_smol_demanding_diego.png")
                if keys[pygame.K_LEFT]:
                    self.penguin.moveUp(0)
                if keys[pygame.K_RIGHT]:
                    self.penguin.moveDown(0)
            else:
                self.penguin.image = pygame.image.load("penguin_smol.png")
                if keys[pygame.K_LEFT]:
                    self.penguin.moveUp(5)
                if keys[pygame.K_RIGHT]:
                    self.penguin.moveDown(5)

            self.all_penguins.update()
            self.boulders.update()
            self.ice_patches.update()
            self.screen.fill(self.WHITE)
            self.screen.blit(timer, (350, 30))
            self.boulders.draw(self.screen)
            self.ice_patches.draw(self.screen)
            self.all_penguins.draw(self.screen)
            self.finish_line_group.draw(self.screen)
            pygame.display.update()
            clock.tick_busy_loop(60)
        pygame.quit()


if __name__ == '__main__':
    game = Sled_Main()
    game.main_loop()
