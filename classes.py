import pygame, sys, random
from pygame.locals import *

SCREENWIDTH = 1500
SCREENHEIGHT = 1000

class Block(pygame.sprite.Sprite):
    def __init__(self, screen, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.speedx = 2

    def update(self):
        self.rect.left -= self.speedx
        if self.rect.right < 0:
            x_displacement = random.randint(0, SCREENWIDTH*2)
            self.rect.x = (SCREENWIDTH + x_displacement)
            self.rect.y = random.randrange(SCREENHEIGHT - 150)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, color, size, increment):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.size = size
        self.image.fill(color)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.increment = increment

    def on_event(self, event):
        if event.type == KEYDOWN:

            if self.rect.y > SCREENHEIGHT-(self.size + self.increment):
                self.rect.y = SCREENHEIGHT - self.size
            elif self.rect.y < SCREENHEIGHT- self.size:
                self.rect.y += self.increment



        elif event.type == MOUSEBUTTONDOWN:
            if self.rect.y < self.increment:
                self.rect.y = 0
            elif self.rect.y > 0:
                self.rect.y -= self.increment

    def collide(self, obstacles, score):
        if pygame.sprite.spritecollide(self, obstacles, False):
            print(int(score))
            pygame.quit()
            sys.exit()



class Game:
    def __init__(self, num_blocks, player_color=(255, 0, 0)):
        pygame.init()

        self.mainSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
        pygame.display.set_caption("Collision Game")
        self.blocksGroup = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.score = 0

        for i in range(num_blocks):
            height = random.randint(30, 150)
            weight = random.randint(30, 150)
            myBlock = Block(mainSurface, (255, 255, 255), weight, height)
            x_displacement = random.randint(0, SCREENWIDTH)
            myBlock.rect.x = (SCREENWIDTH + x_displacement)
            myBlock.rect.y = random.randrange(SCREENHEIGHT - 150)
            self.blocksGroup.add(myBlock)

        self.player = Player(mainSurface, player_color, 50, 20)
        self.player.rect.x = 200
        self.player.rect.y = 0.5*SCREENHEIGHT
        self.player_group.add(player)

    
