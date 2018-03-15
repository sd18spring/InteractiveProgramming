import pygame, sys
from pygame.locals import *
from pygame.font import *
import time
import numpy
import random
import pickle
from os.path import exists

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
            gas.update(model)
            if gas.y>500:
                gas.kill()
        for pedestrian in self.pedestrians:
            pedestrian.update(model)
            if pedestrian.y>500:
                pedestrian.kill()
        for obstacle in self.obstacles:
            obstacle.update(model)
            if obstacle.y>500:
                obstacle.kill()
                self.player.obstacles_avoided+=1
        for line in self.rd_lines:
            line.update(model)
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

class RoadLines(pygame.sprite.Sprite):
    """road lines to simulate the road moving by"""
    def __init__(self, y=0):
        super().__init__()
        self.x = 310
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 40)

    def update(self,model):
        self.y += .50
        if model.player.score > 19:
            self.y += .26
        if model.player.score > 49:
            self.y += .27
        if model.player.score > 74:
            self.y += .28
        if model.player.score > 99:
            self.y += .29
class EnvironmentObject(pygame.sprite.Sprite):
    """base class for objects"""
    def __init__(self,x,y=-30):
        super().__init__()
        self.x = x
        self.y = y

    def update(self,model):
        self.y += .50
        self.rect.x = self.x
        self.rect.y = self.y
        if model.player.score > 19:
            self.y += .26
        if model.player.score > 49:
            self.y += .27
        if model.player.score > 74:
            self.y += .28
        if model.player.score > 99:
            self.y += .29
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
        self.gas_collected = 0
        self.obstacles_avoided = 0
        self.level = 1

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

        if self.score > 19:
            self.level = 2
        if self.score > 49:
            self.level = 3
        if self.score > 74:
            self.level = 4
        if self.score > 99:
            self.level = 5

    def is_collided_with_gas(self, gas_group):
        for gas_sprite in gas_group:
            if self.rect.colliderect(gas_sprite.rect):
                self.gas_level += 5
                self.gas_collected += 1
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
        """initialize model, screen, and HUD elements"""
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
        textsurf1 = myfont.render('Level: '+str(self.model.player.level),
                                  False, (255,255,255))
        self.screen.blit(textsurf1, (25, 410))
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

def main_menu(model):
    """Main menu function"""
    #screen
    screen = pygame.display.set_mode((640,480))
    screen.fill(pygame.Color(255,0,0))
    #title
    title_font = pygame.font.SysFont('Arial', 50)
    title_surf = title_font.render('ROAD RAGE', True, (0,0,0))
    #instructions
    instruction_font = pygame.font.SysFont('Arial', 30)
    instruction_surf1 = instruction_font.render('The game is simple:',True,(0,0,0))
    instruction_surf2 = instruction_font.render('Avoid obstacles.',True,(0,0,0))
    instruction_surf3 = instruction_font.render('Hit pedestrians.',True,(0,0,0))
    instruction_surf4 = instruction_font.render('Dont run out of gas.',True,(0,0,0))
    instruction_surf5 = instruction_font.render('Use the arrow keys to move.',True,(0,0,0))
    instruction_surf6 = instruction_font.render('Press SPACE to start, or Esc to quit.',True,(0,0,0))

    #high score stuff
    high_scores = extract_high_scores(model)
    hs_font = pygame.font.SysFont('Arial', 20)
    hs_title = hs_font.render("Most Hit 'n Runs (so far)",True,(0,0,0))
    hs_1 = hs_font.render(str(high_scores[0]),True,(0,0,0))
    hs_2 = hs_font.render(str(high_scores[1]),True,(0,0,0))
    hs_3 = hs_font.render(str(high_scores[2]),True,(0,0,0))

    running = True
    while running:
        screen.blit(title_surf, (30,100))
        screen.blit(instruction_surf1, (30,150))
        screen.blit(instruction_surf2, (30,180))
        screen.blit(instruction_surf3, (30,210))
        screen.blit(instruction_surf4, (30,240))
        screen.blit(instruction_surf5, (30,270))
        screen.blit(instruction_surf6, (30,300))
        screen.blit(hs_title, (350,50))
        screen.blit(hs_1, (425,70))
        screen.blit(hs_2, (425,90))
        screen.blit(hs_3, (425,110))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    running = False
        pygame.display.update()

def death_screen(model):
    """screen that you see when you die"""
    store_high_scores(model)
    #screen
    screen = pygame.display.set_mode((640,480))
    screen.fill(pygame.Color(255,0,0))
    #title
    msg_font = pygame.font.SysFont('Arial', 50)
    msg_surf = msg_font.render('YOU ARE DEAD', True, (0,0,0))
    #instructions
    stat_font = pygame.font.SysFont('Arial', 30)

    stat_surf1 = stat_font.render('Pedestrians Hit: '+str(model.player.score),
                                   True, (0,0,0))
    high_score_surf = stat_font.render('***NEW HIGH SCORE***', True, (0,0,0))
    stat_surf2 = stat_font.render('Gastanks Collected: '+str(model.player.gas_collected),
                                   True, (0,0,0))
    stat_surf3 = stat_font.render('Obstacles Avoided: '+str(model.player.obstacles_avoided),
                                   True, (0,0,0))
    stat_surf4 = stat_font.render('Level Reached: '+str(model.player.level),
                                   True, (0,0,0))
    #instructions
    instruction_font = pygame.font.SysFont('Arial', 20)
    instruction_surf = instruction_font.render('Press SPACE to restart, press ESC to quit.',
                                   True, (0,0,0))

    running = True
    while running:
        screen.blit(msg_surf, (150,100))
        screen.blit(stat_surf1, (150,150))
        screen.blit(stat_surf2, (150,180))
        screen.blit(stat_surf3, (150,210))
        screen.blit(stat_surf4, (150,240))
        screen.blit(instruction_surf, (150,400))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                if event.key == K_ESCAPE:
                    return pygame.quit()
        pygame.display.update()

def main_game_loop(model,view,controller):
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

def store_high_scores(model):
    """stores top 3 local high scores"""
    filename = 'road_rage_high_scores.pickle'
    current_scores = pickle.load(open(filename,'rb+'))
    if model.player.score > min(current_scores):
        current_scores.pop()
        current_scores.append(model.player.score)
    current_scores.sort(reverse=True)
    pickle.dump(current_scores,open(filename,'wb'))
    return

def extract_high_scores(model):
    """stores top 3 local high scores"""
    filename = 'road_rage_high_scores.pickle'
    if not exists(filename):
        base_hs = [3,2,1]
        pickle.dump(base_hs,open(filename,'wb'))
    return pickle.load(open(filename, 'rb'))


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    running = True
    while running:
        model = Model()
        view = View(model)
        controller = Controller(model)
        main_menu(model)
        main_game_loop(model,view,controller)
        running = death_screen(model)
