import pygame, sys
from pygame.locals import *
from pygame.font import *
import time
import numpy
import random
pygame.init()
pygame.font.init()

class Model(object):
    """keeps track of the game state"""
    def __init__(self):

        self.player = Player(295, 200)
        self.player_group = pygame.sprite.Group()

        self.pedestrians = pygame.sprite.Group()
        self.gastanks = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_objs = pygame.sprite.Group()

        self.rd_lines = pygame.sprite.Group()
        for i in numpy.linspace(0, 520, 12):
            line = RoadLines(i)
            line.add(self.rd_lines)

    def update(self):
        """update positions of objects, player, rd_lines, and adds more
        objects to the arena"""
        self.player.update()
        for gas in self.gastanks:
            gas.update()
            if gas.y>500:
                gas.kill()
        for pedestrian in self.pedestrians:
            pedestrian.update()
            if pedestrian.y>500:
                pedestrian.kill()
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.y>500:
                obstacle.kill()
        for line in self.rd_lines:
            line.update()
            if line.y>520:
                line.y = 0
        self.add_obj()
        self.player.is_collided_with_gas(self.gastanks)
        self.player.is_collided_with_peds(self.pedestrians)
        self.player.is_collided_with_obst(self.obstacles)


    def add_obj(self):
        """Randomly adds objects for the player to interact with"""
        obj_index = random.randint(1,4000)
        if self.player.gas_level < 20:
            if obj_index>3995:
                gas = Gastank(random.randint(20,600))
                if pygame.sprite.spritecollideany(gas, self.all_objs):
                    gas.kill()
                else:
                    gas.add(self.all_objs)
                    gas.add(self.gastanks)

        if obj_index == 1:
            gas = Gastank(random.randint(20,600))
            if pygame.sprite.spritecollideany(gas, self.all_objs):
                gas.kill()
            else:
                gas.add(self.all_objs)
                gas.add(self.gastanks)

        if obj_index > 1 and obj_index < 9:
            ped = Pedestrian(random.randint(20,600))
            if pygame.sprite.spritecollideany(ped, self.all_objs):
                ped.kill()
            else:
                ped.add(self.all_objs)
                ped.add(self.pedestrians)

        if obj_index > 10 and obj_index < 20:
            obst = Obstacle(random.randint(20,520))
            if pygame.sprite.spritecollideany(obst, self.all_objs):
                obst.kill()
            else:
                obst.add(self.all_objs)
                obst.add(self.obstacles)

    def detect_collisions(self):
        """detect collisions between player and objs"""

        objs=pygame.sprite.groupcollide(self.player_group, self.all_objs, False, False)
        if objs:
            for i in objs[self.player]:
                i.kill()


class RoadLines(pygame.sprite.Sprite):
    """road lines to simulate the road moving by"""
    def __init__(self, y=0):
        super().__init__()
        self.x = 310
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 40)

    def update(self):
        self.y += .50


class EnvironmentObject(pygame.sprite.Sprite):
    """base class for objects"""
    def __init__(self,x,y=-30):
        super().__init__()
        self.x = x
        self.y = y

    def update(self):
        self.y += .50
        self.rect.x = self.x
        self.rect.y = self.y

class Gastank(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self,x):
        super().__init__(x)
        #self.rect = pygame.Rect(self.x, self.y, 20, 30)
        self.image = pygame.image.load('gas.png')
        self.image = pygame.transform.scale(self.image, (20,30))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Pedestrian(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self,x):
        super().__init__(x)
        self.image = pygame.image.load('pedestrian.png')
        self.image = pygame.transform.scale(self.image, (20,50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Obstacle(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self,x):
        super().__init__(x)
        self.image = pygame.image.load('road_closed.png')
        self.image = pygame.transform.scale(self.image, (150,50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Player(pygame.sprite.Sprite):
    """user controlled player"""
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.gas_level = 100
        self.score = 0
        self.image = pygame.image.load('car.jpg')
        self.image = pygame.transform.scale(self.image, (50,80))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.alive = True
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        if self.x < 1:
            self.x = 1
            self.x += self.vx
        elif self.x > 589:
            self.x = 589
            self.x += self.vx
        else:
            self.x += self.vx

        if self.y < 1:
            self.y = 1
            self.y += self.vy
        elif self.y > 399:
            self.y = 399
            self.y += self.vy
        else:
            self.y += self.vy

        self.gas_level -= .005
        if self.gas_level < 0:
            self.alive = False

        self.rect.y = self.y
        self.rect.x = self.x

    def is_collided_with_gas(self, gas_group):
        for gas_sprite in gas_group:
            if self.rect.colliderect(gas_sprite.rect):
                self.gas_level += 5
                if self.gas_level > 100:
                    self.gas_level = 100
                gas_sprite.kill()

    def is_collided_with_peds(self, ped_group):
        for ped_sprite in ped_group:
            if self.rect.colliderect(ped_sprite.rect):
                self.score += 1
                ped_sprite.kill()

    def is_collided_with_obst(self, obst_group):
        for obst_sprite in obst_group:
            if self.rect.colliderect(obst_sprite.rect):
                self.alive = False
                



class View():
    """drawing what is in the model"""
    def __init__(self, model):

        self.model = model
        self.screen = pygame.display.set_mode((640,480))
        self.gas_image = pygame.image.load('gas.png')
        self.hud_gas = pygame.transform.scale(self.gas_image, (10,15))
        self.ped_image = pygame.image.load('pedestrian.png')
        self.hud_ped = pygame.transform.scale(self.ped_image, (10,25))


    def draw(self):
        """Draw the current game state on the screen"""
        #drawing the road
        self.screen.fill(pygame.Color(50,50,50))
        pygame.draw.rect(self.screen,
                       pygame.Color(255,255,0),
                       pygame.Rect(10,0,10,480))
        pygame.draw.rect(self.screen,
                       pygame.Color(255,255,0),
                       pygame.Rect(620,0,10,480))
            #drawing scrolling road lines
        for line in self.model.rd_lines:
            pygame.draw.rect(self.screen,
                             pygame.Color(255,255,255),
                             pygame.Rect(line.x,line.y-40,10,40))

        #drawing objects
        for pedestrian in self.model.pedestrians:
            self.screen.blit(pedestrian.image,(pedestrian.x,pedestrian.y))
        for gastank in self.model.gastanks:
            self.screen.blit(gastank.image,(gastank.x,gastank.y))
        for obstacle in self.model.obstacles:
            self.screen.blit(obstacle.image,(obstacle.x,obstacle.y))

        #HUD elements
        myfont = pygame.font.SysFont('Arial', 20)
        textsurf = myfont.render('Score: '+str(self.model.player.score),
                                 False, (255,255,255))
        self.screen.blit(textsurf, (25,430))
        self.screen.blit(self.hud_ped, (120,425))
        pygame.draw.rect(self.screen,
                         pygame.Color(255,0,0),
                         pygame.Rect(25,455,100,10))
        pygame.draw.rect(self.screen,
                         pygame.Color(0,255,0),
                         pygame.Rect(25,455,self.model.player.gas_level,10))
        self.screen.blit(self.hud_gas, (130,452.5))

        #draw player
        self.screen.blit(self.model.player.image, (self.model.player.x,self.model.player.y))

        pygame.display.update()

class Controller(object):
    """keyboard controls"""
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        pygame.key.set_repeat(1,50)
        if event.type != KEYDOWN:
            self.model.player.vx = 0
            self.model.player.vy = 0
        elif event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                self.model.player.vy -= 1
            if event.key == pygame.K_DOWN:
                self.model.player.vy += 1
            if event.key == pygame.K_LEFT:
                self.model.player.vx -= 1
            if event.key == pygame.K_RIGHT:
                self.model.player.vx += 1




class MainMenu():
    """main menu"""
    pass

class PauseMenu():
    """pause menu"""
    pass

FPS = 30
fpsClock = pygame.time.Clock()




if __name__ == "__main__":

    model = Model()
    view = View(model)
    controller = Controller(model)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        if not model.player.alive:
            running = False
        view.draw()
        time.sleep(.001)
    pygame.quit()








#MAIN GAME LOOP:
    #size = (640, 480)
    #screen = pygame.display.set_mode(size)
    #pygame.display.set_caption('ROAD RAGE')
    #running = True
    #while running:
        #for event in pygame.event.get():
            #if event.type == QUIT:
                #running = False
        #time.sleep(.001)

    #pygame.quit()


#testing




#if direction == 'right':
#    carx += 5
#
#    if carx == 350:
#        direction == 'down'
#elif direction == 'down':
#    cary += 5
#    if cary == 480:
#        direction == 'left'
#if direction == 'left':
#    carx += 5

#    if carx == 20:
#        direction == 'up'
#elif direction == 'up':
#    cary += 5
#    if cary == 10:
#        direction == 'right'
