import pygame
from pygame.locals import *
from math import *
import time
import random

# Define some colors
WHITE = (255, 255, 255) # have no idea what it does
BLACK = (0, 0, 0) # need to keep
BLUE = (0, 0, 255)
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([1024,768])

clock = pygame.time.Clock() # I sure this controls the time the game (how faster the puase is at the bottom)

class Player(pygame.sprite.Sprite): # player object right now is confusing do it postion here but not being used
    """ Encodes the state of the paddle in the game """
    def __init__(self,filename, a, b):
        """ Initialize the player and position (x,y) """
        super().__init__()


        self.angle = 0
        self.image = pygame.image.load(filename).convert() #image goes here
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = a;
        self.rect.y = b;

    def update(self):# this may work idk yet
        """ update the state of the paddle """

        self.image_dom = rot_center(self.image, self.angle)

    def __str__(self):
        return "Player, x=%f, y=%f" % (self.x, self.y)

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, angle, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)



        self.speed = 5

        self.angle = angle

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        """ Move the bullet. """
        self.rect.x += self.speed * cos(radians(-self.angle+3))
        self.rect.y += self.speed * sin(radians(-self.angle+3))

class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()

class PyGameKeyboardController(object): #works well a little jumpy maybe use vx
    """ Handles keyboard input for brick breaker """
    def __init__(self):

       self.x = 0
       self.y = 0
       self.j =0
       self.i =0
    def handle_event1(self, event, Player):
        """ Left and right presses modify the x velocity of the paddle """
        #link for event.key https://www.pygame.org/docs/ref/key.html
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_a:
            Player.rect.x += -2
        if event.key == pygame.K_d:
            Player.rect.x += 2
        if event.key == pygame.K_w:
            Player.rect.y += -2
        if event.key == pygame.K_s:
            Player.rect.y += 2
        if event.key == pygame.K_q:
            Player.angle += 1 %360
        if event.key == pygame.K_e:
            Player.angle += -1 %360
        if event.key == pygame.K_2:
            self.i +=1

    def handle_event2(self, event, Player):
        """ Left and right presses modify the x velocity of the paddle """
        #link for event.key https://www.pygame.org/docs/ref/key.html
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_j:
            Player.rect.x += -2
        if event.key == pygame.K_l:
            Player.rect.x += 2
        if event.key == pygame.K_i:
            Player.rect.y += -2
        if event.key == pygame.K_k:
            Player.rect.y += 2
        if event.key == pygame.K_u:
            Player.angle += 1 %360
        if event.key == pygame.K_o:
            Player.angle += -1 %360
        if event.key == pygame.K_8:
            self.j +=1



# Before the loop, load the sounds:
#click_sound = pygame.mixer.Sound("laser5.ogg")
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image



all_sprites_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics only back grond
background_image = pygame.image.load("NewBackground.jpg").convert()

for i in range(100):
    # This represents a block
    block = Block(BLUE)

    # Set a random location for the block 1024,768
    block.rect.x = random.randrange(1024)
    block.rect.y = random.randrange(768)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)



clock = pygame.time.Clock()

score = 0
player1 = Player("BlueTank.png", 0, 0)
player2 = Player("RedTank.png", 100, 100)
#all_sprites_list.add(player)
controller = PyGameKeyboardController()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # Copy image to screen:
    screen.blit(background_image, background_position)


    controller.handle_event1(event,player1)
    controller.handle_event2(event,player2)
    player1.update()
    player2.update()
    all_sprites_list.update()

    if controller.i > 0:
        bullet = Bullet(player1.angle,player1.rect.center[0],player1.rect.center[1])
        all_sprites_list.add(bullet)
        bullet_list.add(bullet)
        controller.i += -1
    if controller.j > 0:
        bullet = Bullet(player2.angle,player2.rect.center[0],player2.rect.center[1])
        all_sprites_list.add(bullet)
        bullet_list.add(bullet)
        controller.j += -1


    screen.blit(player1.image_dom, [player1.rect.x, player1.rect.y])
    screen.blit(player2.image_dom, [player2.rect.x, player2.rect.y])
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    all_sprites_list.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
