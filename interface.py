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
crashed = False
shipImg = pygame.image.load('spa.png')

class Ship():
    x_speed = 0
    y_speed = 0
    def __init__(self,x,y,angle,img):
        self.angle = angle
        self.x = x
        self.y = y
        self.image = img
    def move(self):
        self.x_speed += math.cos(math.radians(self.angle))*2
        self.y_speed += math.sin(math.radians(self.angle))*2

    def rotate(self,posNeg):
        self.image = pygame.transform.rotate(self.image,5*posNeg)
        self.angle += posNeg*5

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        gameDisplay.blit(self.image,(self.x,self.y))


shipX = (display_width * .5)
shipY = (display_height * .5)

ship = Ship(shipX,shipY,315,shipImg)

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        #print(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.move()
            if event.key == pygame.K_LEFT:
                ship.rotate(1)

    gameDisplay.fill(white)

    ship.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
