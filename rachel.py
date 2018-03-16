#THIS FILE IS DOPE
import pygame
from pygame.locals import *
import time
from random import *
clock = pygame.time.Clock()

class Penguin(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load("penguin_smol.png")
        self.rect = self.image.get_rect()
    def moveUp(self, pixels):
        if self.rect.y <= 0:
            self.rect.y = 0
        else:
            self.rect.y -= pixels
    def moveDown(self, pixels):
        if self.rect.y >= 340:
            self.rect.y = 340
        else:
            self.rect.y += pixels

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, image_name, rect = None):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect

    def moveLeft(self, pixels = 5):
        self.rect.x -= pixels
    def slowDown(self, pixels = 1):
        self.rect.x -= pixels
    def speedUp(self, pixels = 7):
        self.rect.x -= pixels

class Powerups(Obstacles):
    def speedUp(self, pixels = 7):
        self.rect.x -= pixels

class FinishLine(Obstacles):
    pass

class Bump(Obstacles):
    def slowDown(self, pixels = 3):
        self.rect.x -= pixels

class KeyController(object):
    def __init__(self, model):
        self.model = model

    def event_type(self, keys, state):
        if keys[pygame.K_LEFT] and state == 1:
            self.model.penguin.moveUp(0)
        if keys[pygame.K_RIGHT] and state == 1:
            self.model.penguin.moveDown(0)
        if keys[pygame.K_LEFT] and state == 2:
            self.model.penguin.moveUp(5)
        if keys[pygame.K_RIGHT] and state == 2:
            self.model.penguin.moveDown(5)

class CPSledView(object):
    def __init__(self, model, width, height):
        self.model = model
        size = (width, height) #viewing frame is 500 x 400 pixels
        self.model.WHITE = pygame.Color(255, 255, 255)
        self.model.screen = pygame.display.set_mode(size)
        #self.model.pygame.display.set_caption("Club Penguing Sledding Game")

    def draw(self, model, timer):
        self.model = model
        self.model.screen.blit(timer, (425, 20))
        self.model.boulders.draw(self.model.screen)
        self.model.ice_patches.draw(self.model.screen)
        self.model.bumps.draw(self.model.screen)
        self.model.all_penguins.draw(self.model.screen)
        self.model.finish_line_group.draw(self.model.screen)
        pygame.display.update()

class CPSledModel(object):
    def __init__(self, width, height):
        pygame.init()
        size = (width, height) #viewing frame is 500 x 400 pixels
        self.WHITE = pygame.Color(255, 255, 255)
        self.screen = pygame.display.set_mode(size)
        self.height = height
        self.width = width

    def loadSprites(self):
        self.penguin = Penguin()
    #    self.penguin.image = pygame.transform.rotate(self.penguin.image, -30)
        self.all_penguins = pygame.sprite.RenderPlain(self.penguin)
        self.boulders = pygame.sprite.RenderPlain()
        self.ice_patches = pygame.sprite.RenderPlain()
        self.finish_line_group = pygame.sprite.RenderPlain()
        self.bumps = pygame.sprite.RenderPlain()

        for num_boulders in range(20):
            x_position = (num_boulders+1) * 400 #randint(260, 360)
            y_boulders = randint(1,3)
            for i in range(y_boulders):
                y_position = randrange(0, 340, 70)
                self.boulder = Obstacles("rock.png", pygame.Rect(x_position, y_position, 60, 60))
                self.boulder.rect.inflate(0, -10)
                self.boulders.add(self.boulder)

        for num_ice_patches in range(8):
            x_position = (num_ice_patches+1) * 560 #randint(260, 360)
            y_position = randint(0, 340)
            self.ice_patch = Powerups("ice_patch_flat.png", pygame.Rect(x_position, y_position, 280, 70))
            self.ice_patches.add(self.ice_patch)

        for num_bumps in range(7):
            x_position = (num_bumps + 1) * 630
            y_position = randint(0, 400)
            self.bump = Obstacles("bump.png", pygame.Rect(x_position, y_position, 132, 98))
            self.bumps.add(self.bump)

        self.finish_line = FinishLine("finish_line.png", pygame.Rect(6000, -2, 144, 404))
        self.finish_line_group.add(self.finish_line)

    def update(self):
        self.all_penguins.update()
        self.boulders.update()
        self.ice_patches.update()
        self.bumps.update()
        self.screen.fill(self.WHITE)

if __name__ == '__main__':

    def main_loop():
        pygame.init()
        model = CPSledModel(500,400)
        view = CPSledView(model, 500, 400)
        controller = KeyController(model)
        model.loadSprites()
        list_of_obstacles = model.boulders.sprites()
        list_of_obstacles.extend(model.ice_patches.sprites())
        list_of_obstacles.append(model.finish_line)
        list_of_obstacles.extend(model.bumps.sprites())

        font = pygame.font.Font(None, 32)
        pygame.display.set_caption("Club Penguin Sledding Game")
        running = True
        while running:
            current_time = str(pygame.time.get_ticks()/1000)
            timer = font.render(current_time, True, (0,0,0))
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False

            if model.penguin.rect.left > model.finish_line.rect.left+120:
                break

            hit = False
            ice = False
            finish = False
            bump = False
            for obstacle in list_of_obstacles:
                if model.penguin.rect.colliderect(obstacle.rect):
                    hit = True
                    if type(obstacle) == Powerups:
                        ice = True
                    elif type(obstacle) == FinishLine:
                        finish = True
            for obstacle in list_of_obstacles:
                if ice or finish:
                    obstacle.speedUp()
                elif hit:
                    obstacle.slowDown()
                else:
                    obstacle.moveLeft()
            if hit and not ice and not finish:
                model.penguin.image = pygame.image.load("fallen_penguin_smol_demanding_diego.png")
                controller.event_type(pygame.key.get_pressed(), 1)
            else:
                model.penguin.image = pygame.image.load("penguin_smol.png")
                controller.event_type(pygame.key.get_pressed(), 2)

            model.update()
            view.draw(model, timer)
            clock.tick_busy_loop(60)
        pygame.quit()

    main_loop()
