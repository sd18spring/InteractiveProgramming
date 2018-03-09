import GameView
import model
import pygame
from pygame.locals import *
import time
if __name__ == "__main__":
    model = model.Model()
    print(model.terrains[0])
    view = GameView.GameView(model, (1000,1000))
    running = True
    while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            time.sleep(.001)
            view.draw()
    pygame.quit
