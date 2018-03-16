#THIS FILE IS DOPE
import pygame
from pygame.locals import *
import time
from random import *
clock = pygame.time.Clock()

class Penguin(pygame.sprite.Sprite):
    """
    Penguin is the sprite that the user controls using the left and right arrows
    It moves up and down the screen
    """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load("penguin_smol.png")
        self.rect = self.image.get_rect()
        self.rect.y = 170

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
    """
    Obstacles is the parent class of the many different types of obstacles
    The obstacles continuously move towards the left of the screen (at varying speeds),
    giving the impression that the penguin is moving towards the right of the screen
    """
    def __init__(self, image_name, rect = None):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect

    def moveLeft(self, pixels = 7):
        self.rect.x -= pixels
    def slowDown(self, pixels = 3):
        self.rect.x -= pixels
    def speedUp(self, pixels = 10):
        self.rect.x -= pixels

class Powerups(Obstacles):
    """
    PowerUps inherits from Obstacles and makes the obstacles move faster across the screen,
    making it seem like the penguin is speeding up
    """
    def speedUp(self, pixels = 10):
        self.rect.x -= pixels

class FinishLine(Obstacles):
    pass

class Bump(Obstacles):
    pass

class Log(Obstacles):
    pass

class Ramp(Obstacles):
    pass

class KeyController(object):
    """
    allows the player to move the penguin using the left and right keys
    """
    def __init__(self, model):
        self.model = model

    def event_type(self, keys, state): #state determines whether the penguin hit an obstacle or powerup
        if keys[pygame.K_LEFT] and state == 1:
            #if penguin hits obstacle, prevent the player from moving off the obstacle by "disabling" the keyboard controls
            self.model.penguin.moveUp(0)
        if keys[pygame.K_RIGHT] and state == 1:
            self.model.penguin.moveDown(0)
        if keys[pygame.K_LEFT] and state == 2:
            #if the penguin hits a powerup, the player can still potentially move off the powerup (just to add a bit more challenge)
            self.model.penguin.moveUp(5)
        if keys[pygame.K_RIGHT] and state == 2:
            self.model.penguin.moveDown(5)

class CPSledView(object):
    """
    View class draws all the sprites/screens that the model class updates
    """
    def __init__(self, model, width, height):
        self.model = model
        size = (width, height) #viewing frame is 500 x 400 pixels
        self.model.WHITE = pygame.Color(255, 255, 255)
        self.model.screen = pygame.display.set_mode(size)

    def draw(self, model, timer):
        self.model = model
        self.model.screen.blit(timer, (425, 20))
        self.model.boulders.draw(self.model.screen)
        self.model.ice_patches.draw(self.model.screen)
        self.model.bumps.draw(self.model.screen)
        self.model.logs.draw(self.model.screen)
        self.model.ramps.draw(self.model.screen)
        self.model.all_penguins.draw(self.model.screen)
        self.model.finish_line_group.draw(self.model.screen)
        pygame.display.update()

class CPSledModel(object):
    """
    Model class updates as the player control the sprite
    Creates all the sprites
    Randomly generates a track of obstacles
    """
    def __init__(self, width, height):
        pygame.init()
        size = (width, height)
        self.WHITE = pygame.Color(255, 255, 255)
        self.screen = pygame.display.set_mode(size)
        self.height = height
        self.width = width

    def loadSprites(self):
        self.penguin = Penguin()
        #self.penguin.image = pygame.transform.rotate(self.penguin.image, -30)
        self.all_penguins = pygame.sprite.RenderPlain(self.penguin)
        self.boulders = pygame.sprite.RenderPlain()
        self.ice_patches = pygame.sprite.RenderPlain()
        self.finish_line_group = pygame.sprite.RenderPlain()
        self.bumps = pygame.sprite.RenderPlain()
        self.logs = pygame.sprite.RenderPlain()
        self.ramps = pygame.sprite.RenderPlain()

        for num_boulders in range(18): #creating 20 boulders
            x_position = (num_boulders+1) * randint(410, 440) #randomly generate an x-position within a certain range
            y_boulders = randint(1,3) #randomly decide how many boulders to put in a straight line
            for i in range(y_boulders):
                y_position = randrange(0, 340, 70) #randomly choose a y-position for each boulder
                self.boulder = Obstacles("rock.png", pygame.Rect(x_position, y_position, 60, 60))
                self.boulder.rect.inflate(0, -10)
                self.boulders.add(self.boulder) #add boulder to the boulder sprite group

        for num_ice_patches in range(13):
            x_position = (num_ice_patches+1) * randint(640, 670)
            y_position = randint(0, 340)
            self.ice_patch = Powerups("ice_patch_flat.png", pygame.Rect(x_position, y_position, 280, 70))
            self.ice_patches.add(self.ice_patch)

        for num_bumps in range(12):
            x_position = (num_bumps + 1) * randint(710, 730)
            y_position = randint(0, 300)
            self.bump = Bump("bump.png", pygame.Rect(x_position, y_position, 132, 98))
            self.bumps.add(self.bump)

        for num_logs in range(6):
            x_position = (num_logs+1) * 1100
            y_position = 0
            self.log = Log("log.png", pygame.Rect(x_position, y_position, 170, 400))
            self.logs.add(self.log)
            self.ramp = Ramp("log_jump_test.png", pygame.Rect(x_position, 110,  170, 167))
            self.ramps.add(self.ramp)

        self.finish_line = FinishLine("finish_line.png", pygame.Rect(8750, -2, 144, 404))
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
        #create a master list of all the randomly generated obstacles
        list_of_obstacles = model.boulders.sprites()
        list_of_obstacles.extend(model.ice_patches.sprites())
        list_of_obstacles.extend(model.bumps.sprites())
        list_of_obstacles.extend(model.logs.sprites())

        #this loop parses through the master obstacle list and removes any obstacle that collides with another obstacle to minimize overlapping obstacles
        index = 0
        while index < (len(list_of_obstacles) - 1):
            j = index + 1
            while j < (len(list_of_obstacles) - 1):
                if list_of_obstacles[index].rect.colliderect(list_of_obstacles[j].rect):
                    list_of_obstacles.pop(j)
                    j -= 1
                j += 1
            index += 1

        list_of_obstacles.extend(model.ramps.sprites())
        list_of_obstacles.append(model.finish_line)
        
        font = pygame.font.Font(None, 32)
        pygame.display.set_caption("Club Penguin Sledding Game")
        running = True
        while running:
            #run a timer of how long the penguin takes to get to the finish line
            current_time = str(pygame.time.get_ticks()/1000)
            timer = font.render(current_time, True, (0,0,0))
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False

            #if peguin passes the finish line, then break out of loop
            if model.penguin.rect.left > model.finish_line.rect.left+120:
                while True:
                    for event in pygame.event.get():
                        if event.type is pygame.QUIT:
                            pygame.quit()
                        running = False

            #different flags to identify which obstacle hit
            hit = False
            ice = False
            finish = False
            bump = False
            ramp = False
            for obstacle in list_of_obstacles:
                if model.penguin.rect.colliderect(obstacle.rect):
                    hit = True
                    if type(obstacle) == Ramp:
                        ramp = True
                    if type(obstacle) == Powerups:
                        ice = True
                    elif type(obstacle) == FinishLine:
                        finish = True
                    elif type(obstacle) == Bump:
                        bump = True

            #using the flags, determine how the penguin responds to the obstacle hit
            for obstacle in list_of_obstacles:
                if ramp:
                    obstacle.moveLeft()
                elif ice or finish:
                    obstacle.speedUp()
                elif hit:
                    if bump:
                        obstacle.slowDown(5)
                    else:
                        obstacle.slowDown()
                else:
                    obstacle.moveLeft()
            if hit and not ice and not finish and not ramp:
                if not bump:
                    model.penguin.image = pygame.image.load("fallen_penguin_smol_demanding_diego.png")
                    controller.event_type(pygame.key.get_pressed(), 1)
                else:
                    controller.event_type(pygame.key.get_pressed(), 2)
            else:
                model.penguin.image = pygame.image.load("penguin_smol.png")
                controller.event_type(pygame.key.get_pressed(), 2)

            model.update()
            view.draw(model, timer)
            clock.tick_busy_loop(60)
        pygame.quit()

    main_loop()
