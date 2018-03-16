import GameView
import model
import pygame
from pygame.locals import *
import time
if __name__ == "__main__":
    model = model.Model()
    view = GameView.GameView(model, (1000,1000))
    running = True
    left, up, down, right = False, False, False, False
    while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            time.sleep(.001)
            view.draw()
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
            if event.type == KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
            if(left):
                model.char.accelerate(-1)
            if(right):
                model.char.accelerate(1)
            if(right == False and left == False):
                if(model.char.vel_x > 0):
                    model.char.accelerate(-1)
                    if(model.char.vel_x < 0):
                        model.char.vel_x = 0
                elif(model.char.vel_x < 0):
                    model.char.accelerate(1)
                    if(model.char.vel_x < 0):
                        model.char.vel_x = 0
            print(model.char.vel_x)
            model.char.move()

    pygame.quit
