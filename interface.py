"""
Asteroids via Pygame

@authors coreyacl & nathanestill

"""

import pygame
import math

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

class Ship():
    x_speed = 0
    y_speed = 0
    def __init__(self,x,y,angle,img):
        self.angle = angle
        self.x = x
        self.y = y
        self.image = img
        self.w,self.h = img.get_size()
    def move(self):
        if math.sqrt(self.x_speed**2+self.y_speed**2) < 8:
            self.x_speed += math.cos(math.radians(self.angle))*2
            self.y_speed += math.sin(math.radians(self.angle))*2

    def drift(self):
        """
        Drifts the ship to a stop. Doesn't work yet
        """
        if math.sqrt(self.x_speed**2+self.y_speed**2) > 0:
            self.x_speed = -self.x_speed/10
            self.y_speed = -self.y_speed/10
        else:
            self.x_speed = 0
            self.y_speed = 0

    def rotate(self,posNeg):
        self.image = pygame.transform.rotate(self.image,5*posNeg)
        self.angle += posNeg*5

    def update(self):
        width,height = gameDisplay.get_size()

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

ship = Ship(shipX,shipY,315,shipImg)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #print(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.move()
            if event.key == pygame.K_LEFT:
                ship.rotate(1)
            if event.key == pygame.K_RIGHT:
                ship.rotate(-1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ship.drift()

    gameDisplay.fill(white)

    ship.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
