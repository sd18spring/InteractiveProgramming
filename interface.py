"""
Asteroids via Pygame

@authors coreyacl & nathanestill

"""

import pygame
from math import cos,sin,sqrt,radians,atan

pygame.init()

display_width = 1000
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Asteroids")

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
running = True
shipImg = pygame.image.load('spa.png')

def rot_center(image, angle):
    """rotate an image while keeping its center and size
    Found online. Very helpful
    """

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Ship():
    """Ship class!
    Holds data on ship:
    angle (degress)
    x_speed
    y_speed
    x (position)
    y (position)
    image
    drift (boolean)

    """
    x_speed = 0
    y_speed = 0
    drift = False
    def __init__(self,x,y,angle,img):
        """
        Initliazes with where the ship is facing as the angle
        """
        self.angle = angle
        self.x = x
        self.y = y
        self.image = img
        self.w,self.h = img.get_size()
    def move(self):
        """FORWARD!!!
        Moves the ship forward in the direction it's heading (its angle)
        """
        ship.drift = False
        if sqrt(self.x_speed**2+self.y_speed**2) < 10:
            self.x_speed += cos(radians(self.angle))*2
            self.y_speed += sin(radians(self.angle))*2

    def rotate(self,posNeg):
        """Rotates ship"""
        self.image = rot_center(self.image,posNeg*35)
        #self.image = pygame.transform.rotate(self.image,35*posNeg)
        self.angle -= posNeg*35
        # speed = sqrt(self.x_speed**2+self.y_speed**2)
        # self.x_speed = cos(radians(self.angle))*speed
        # self.y_speed = sin(radians(self.angle))*speed



    def update(self):
        """MAGIC
        Does magic and makes the ship work.
        Updates position
        """
        width,height = gameDisplay.get_size()
        if self.drift:
            speed = sqrt(self.x_speed**2+self.y_speed**2)*.02
            theta = atan(self.y_speed/self.x_speed)
            self.x_speed -= cos(theta)*speed
            self.y_speed -= sin(theta)*speed
        if sqrt(self.x_speed**2+self.y_speed**2) < .02:
            self.x_speed = 0
            self.y_speed = 0
            self.drift = False
        if sqrt(self.x_speed**2+self.y_speed**2) > 10:
            self.drift = False
            self.x_speed = cos(radians(self.angle))
            self.y_speed = sin(radians(self.angle))
        self.x += self.x_speed
        self.y += self.y_speed

        if(self.x >= width):
            self.x = 0 - self.w
        elif(self.x <= 0 - self.w):
            self.x = width
        if(self.y >= height):
            self.y = 0 - self.h
        elif(self.y <= 0 - self.h):
            self.y = height

        gameDisplay.blit(self.image,(self.x,self.y))


shipX = (display_width * .5)
shipY = (display_height * .5)
w,h = shipImg.get_size()
shipImg = pygame.transform.scale(shipImg,(int(w*.5),int(h*.5)))
ship = Ship(shipX,shipY,315,shipImg)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # print(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.move()
            if event.key == pygame.K_LEFT:
                ship.rotate(1)
            if event.key == pygame.K_RIGHT:
                ship.rotate(-1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ship.drift = True
            if event.key == pygame.K_q:
                running = False

    gameDisplay.fill(white)

    ship.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
