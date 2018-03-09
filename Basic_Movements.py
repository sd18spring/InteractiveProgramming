import pygame
from pygame.locals import *

#Initialize the screen
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Smash Clone")


clock = pygame.time.Clock()
FPS = 120

#Variable to keep the game running
running = True

#the sample rectangle, danny
danny =  pygame.rect.Rect((20, 20, 250, 100))
print(danny)

#booleans for control toggles.
left = False
right = False
up = False
down = False

while running:
    #make the background pretty close to black
    screen.fill((0, 15, 15))

    #For each event at the moment:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #KEYDOWN events toggle movement on
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True
        #KEYUP events toggles movement off
        if event.type == KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False
    #actually moving the rectangle. move() is a fruitful function
    if left:
        danny = danny.move(-10, 0)
    if right:
        danny = danny.move(10, 0)
    if up:
        danny = danny.move(0, -10)
    if down:
        danny = danny.move(0, 10)

    #drawing the rectangle to the screen, and updating the screen
    pygame.draw.rect(screen, [255, 255 ,255], danny)
    pygame.display.update()
    #clock for consistent for loop timing.
    clock.tick(FPS)

pygame.quit()
