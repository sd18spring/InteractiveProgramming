import pygame
import model
import terrain
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
        pygame.draw.rect(self.screen, pygame.Color(100,100,100), pygame.Rect(self.model.char.pos_x, self.model.char.pos_y, self.model.char.width, self.model.char.height))
        pygame.display.update()
