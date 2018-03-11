import pygame
import terrain
from character import Character
from model import Model
from pygame.locals import *
class GameView:
    def __init__(self, model, size):
        self.model = model
        self.size = size
        self.screen = pygame.display.set_mode(size)


    def draw(self):
        """
        Updates graphics to game screen
        """
        self.screen.fill(pygame.Color(200,210,255))
        for t in self.model.terrains:
            pygame.draw.rect(self.screen, pygame.Color(150,120,10), pygame.Rect(t.pos[0],t.pos[1],t.size[0], t.size[1]))
        for char in self.model.characters:
            pygame.draw.rect(self.screen, pygame.Color(100,100,100), char.rect)
            pygame.draw.rect(self.screen, pygame.Color(100,100,100), char.attack_rect)
        pygame.display.update()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    FPS = 30

    char1 = Character(pos_x = 500, pos_y = 500, label = 'char1')
    char2 = Character(label = 'char2')
    model = Model(char1, char2)
    view = GameView(model, (1000, 1000))
    while model.game_running:
        for event in pygame.event.get():
            model.quit(event)
            for char in model.characters:
                model.x_movement(event, char)
                model.y_movement(event, char)
                model.attack_command(event, char)
        model.update_motion()
        view.draw()
        clock.tick(FPS)
