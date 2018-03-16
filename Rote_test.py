import pygame
from pygame.locals import *
from math import *
import time

# Define some colors
WHITE = (255, 255, 255) # have no idea what it does
BLACK = (0, 0, 0) # need to keep

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([600, 361])

clock = pygame.time.Clock() # I sure this controls the time the game (how faster the puase is at the bottom)

class Player(pygame.sprite.Sprite): # player object right now is confusing do it postion here but not being used
    """ Encodes the state of the paddle in the game """
    def __init__(self):
        """ Initialize the player and position (x,y) """
        super().__init__()

        #self.x = 30
        #self.y = 30
        self.angle = 0
        self.old_angle = 0
        self.image = pygame.image.load("top_down_tank-8hkMRt.png").convert() #image goes here
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 0;
        self.rect.y = 0;

    def update(self):# this may work idk yet
        """ update the state of the paddle """
        #self.rect.x += self.x
        # self.rect.y += self.y
        #self.image_dom = pygame.transform.rotate(self.image, self.angle)
        self.image = rot_center(self.image, self.angle - self.old_angle)
        self.old_angle=self.angle
    def __str__(self):
        return "Player, x=%f, y=%f" % (self.x, self.y)

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, angle, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)

        #self.player = Player

        self.speed = 5
        #self.x = self.player.x
        #self.y = self.player.y
        self.angle = angle

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        """ Move the bullet. """
        self.rect.x += self.speed * cos(radians(-self.angle+3))
        self.rect.y += self.speed * sin(radians(-self.angle+3))
        #screen.blit(bullet.image, [self.x, self.y])

class PyGameKeyboardController(object): #works well a little jumpy maybe use vx
    """ Handles keyboard input for brick breaker """
    def __init__(self):
       #self.model = model
       self.x = 0
       self.y = 0
       #self.Player = Player
       self.i =0
    def handle_event(self, event, Player):
        """ Left and right presses modify the x velocity of the paddle """
        #link for event.key https://www.pygame.org/docs/ref/key.html

        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_a:
            Player.rect.x += -10
        if event.key == pygame.K_d:
            Player.rect.x += 10
        if event.key == pygame.K_w:
            Player.rect.y += -10
        if event.key == pygame.K_s:
            Player.rect.y += 10
        if event.key == pygame.K_q:
            Player.angle += 1 %360
        if event.key == pygame.K_e:
            Player.angle += -1 %360
        if event.key == pygame.K_2:
            self.i +=1
            print(self.i)
            print('pew')

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

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics only back grond
background_image = pygame.image.load("GrassBackground.jpg").convert()
#all_sprites_list.add(background_image)



clock = pygame.time.Clock()

player = Player()
all_sprites_list.add(player)
controller = PyGameKeyboardController()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # Copy image to screen:
    screen.blit(background_image, background_position)


    controller.handle_event(event,player)
    player.update()
    all_sprites_list.update()
    if controller.i > 0:
        bullet = Bullet(player.angle,player.rect.center[0],player.rect.center[1])
        all_sprites_list.add(bullet)

        #screen.blit(bullet.image, [bullet.x, bullet.y])
        controller.i += -1
    #player.image1 = pygame.transform.rotate(player.image, 10)
    #player.image = rot_center(player.image, 1)
    # Copy image to screen:
    #screen.blit(player.image_dom, [player.rect.x, player.rect.y])

    all_sprites_list.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
