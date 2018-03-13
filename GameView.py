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
            pygame.draw.rect(self.screen, pygame.Color(150,120,10), t.rect)
        for char in self.model.characters:
            if(char.left):
                self.screen.blit(char.left_img, char.rect)
            elif(char.right):
                self.screen.blit(char.right_img, char.rect)
            elif (char.vel_y < 0):
                self.screen.blit(char.down_img, char.rect)
            else:
                self.screen.blit(char.up_img, char.rect)
            for i in range (char.lives):
                self.screen.blit(char.up_img, (570 + 120 * i, 950 - char.player * 150))
            #pygame.draw.rect(self.screen, pygame.Color(100,100,100), char.attack_rect)
        pygame.display.update()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    FPS = 30

    char1 = Character(pos_x = 1200, label = 'char1')
    char2 = Character(label = 'char2', keys = {"left": pygame.K_a, "right": pygame.K_d, "up" : pygame.K_w, "down":
                                                pygame.K_s, "attack" : pygame.K_x},
                                                left_img = "left2.png",
                                                right_img = "right2.png",
                                                up_img = "up2.png",
                                                down_img = "down2.png",
                                                player = 2)
    model = Model(char1, char2)
    view = GameView(model, (1500, 1000))
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
