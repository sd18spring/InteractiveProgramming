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
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 120)
        self.textsurface = self.font.render('GAME OVER', False, (0, 0, 0))
    def draw(self):
        """
        Updates graphics to game screen
        """
        self.screen.fill(pygame.Color(200,210,255))
        for t in self.model.terrains:
            pygame.draw.rect(self.screen, pygame.Color(150,120,10), t.rect)
        for char in self.model.characters:
            if char.attacking:

                self.screen.blit(char.attack_img, char.attack_rect)
            if char.shielding:
                self.screen.blit(char.shield_img, char.rect)
            elif(char.left):
                self.screen.blit(char.left_img, char.rect)
            elif(char.right):
                self.screen.blit(char.right_img, char.rect)
            elif (char.vel_y < 0):
                self.screen.blit(char.down_img, char.rect)
            else:
                self.screen.blit(char.up_img, char.rect)
            for i in range (char.lives):
                self.screen.blit(char.up_img, (570 + 120 * i, 950 - char.player * 150))
        if model.game_over:
            self.screen.blit(self.textsurface,(400,100))
        pygame.display.update()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    FPS = 30

    char1 = Character(label = 'char1')
    char2 = Character(pos_x = 1200, label = 'char2', keys = {"left": pygame.K_j, "right": pygame.K_l, "up" : pygame.K_i, "down":
                                                pygame.K_k, "attack" : pygame.K_o},
                                                left_img = "left2.png",
                                                right_img = "right2.png",
                                                up_img = "up2.png",
                                                down_img = "down2.png",
                                                shield_img = "shield2.png",
                                                player = 2)
    model = Model(char1, char2)
    view = GameView(model, (1500, 1000))
    while model.game_running:
        for event in pygame.event.get():
            model.quit(event)
            if not model.game_over:
                for char in model.characters:
                    model.x_movement(event, char)
                    model.y_movement(event, char)
                    model.attack_command(event, char)
                    model.shield(event, char)
        model.check_lives()
        model.update_motion()
        view.draw()
        clock.tick(FPS)
