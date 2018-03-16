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

        #adding the player to the model
        self.player = Player(295, 200)

        #Groups to keep track of sprite objects
        self.pedestrians = pygame.sprite.Group()
        self.gastanks = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_objs = pygame.sprite.Group()

        #adding road lines to a group
        self.rd_lines = pygame.sprite.Group()
        for i in numpy.linspace(0, 520, 12):
            line = RoadLines(i)
            line.add(self.rd_lines)

    def update(self):
        """update positions of objects, player, rd_lines, and adds more
        objects to the arena"""
        #update player
        self.player.update()

        #update every sprite in gas group and kill it if it moves out of bounds
        for gas in self.gastanks:
            gas.update(model)
            if gas.y>500:
                gas.kill()

        #update every sprite in ped group and kill it if it moves out of bounds
        for pedestrian in self.pedestrians:
            pedestrian.update(model)
            if pedestrian.y>500:
                pedestrian.kill()

        #update every sprite in obst group and kill it if it moves out of bounds
        for obstacle in self.obstacles:
            obstacle.update(model)
            if obstacle.y>500:
                obstacle.kill()
                #update stat
                self.player.obstacles_avoided+=1

        #update road lines and cycle them back to the beginning if out of bounds
        for line in self.rd_lines:
            line.update(model)
            if line.y>520:
                line.y = 0

        #randomly add objs, and detect collisions between player and objs
        self.add_obj()
        self.player.is_collided_with_gas(self.gastanks)
        self.player.is_collided_with_peds(self.pedestrians)
        self.player.is_collided_with_obst(self.obstacles)

    def add_obj(self):
        """Randomly adds objects for the player to interact with"""
        #get random integer
        obj_index = random.randint(1,4000)

        #increase gas output if gas level is low
        if self.player.gas_level < 20:
            if obj_index>3995:
                gas = Gastank(random.randint(20,600))
                #if gas object would collide with another object outside
                #of screen it is not placed
                if pygame.sprite.spritecollideany(gas, self.all_objs):
                    gas.kill()
                else:
                    gas.add(self.all_objs)
                    gas.add(self.gastanks)

        if obj_index == 1 or obj_index==9:
            gas = Gastank(random.randint(20,600))
            #if gas object would collide with another object outside
            #of screen it is not placed
            if pygame.sprite.spritecollideany(gas, self.all_objs):
                gas.kill()
            else:
                gas.add(self.all_objs)
                gas.add(self.gastanks)

        if obj_index > 1 and obj_index < 9:
            ped = Pedestrian(random.randint(20,600))
            #if ped object would collide with another object outside
            #of screen it is not placed
            if pygame.sprite.spritecollideany(ped, self.all_objs):
                ped.kill()
            else:
                ped.add(self.all_objs)
                ped.add(self.pedestrians)

        if obj_index > 10 and obj_index < 18:
            obst = Obstacle(random.randint(20,520))
            #if obst object would collide with another object outside
            #of screen it is not placed
            if pygame.sprite.spritecollideany(obst, self.all_objs):
                obst.kill()
            else:
                obst.add(self.all_objs)
                obst.add(self.obstacles)

class RoadLines(pygame.sprite.Sprite):
    """road lines to simulate the road moving by"""
    def __init__(self, y=0):
        """inherited sprite attributes, position, and rect"""
        super().__init__()
        self.x = 310
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 40)

    def update(self,model):
        """all objects move the same, use similar rect attributes"""
        self.y += .50

        #increase scrolling speed as level increases
        if model.player.score > 10:
            self.y += .1
        if model.player.score > 20:
            self.y += .15
        if model.player.score > 35:
            self.y += .2
        if model.player.score > 50:
            self.y += .25
        if model.player.score > 75:
            self.y += .3
        if model.player.score > 100:
            self.y += .35

class EnvironmentObject(pygame.sprite.Sprite):
    """base class for objects"""
    def __init__(self,x,y=-30):
        """inherited sprite attributes and position"""
        super().__init__()
        self.x = x
        self.y = y

    def update(self,model):
        """all objects move the same, use similar rect attributes"""
        self.y += .50
        self.rect.x = self.x
        self.rect.y = self.y

        #increase movement speed as levels go up
        if model.player.score > 10:
            self.y += .1
        if model.player.score > 20:
            self.y += .15
        if model.player.score > 35:
            self.y += .2
        if model.player.score > 50:
            self.y += .25
        if model.player.score > 75:
            self.y += .3
        if model.player.score > 100:
            self.y += .35

class Gastank(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self,x):
        """inherited, image, and rect attributes"""
        super().__init__(x)
        self.image = pygame.image.load('gas.png')
        self.image = pygame.transform.scale(self.image, (20,30))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Pedestrian(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self,x):
        """inherited, image, and rect attributes"""
        super().__init__(x)
        self.image = pygame.image.load('pedestrian.png')
        self.image = pygame.transform.scale(self.image, (20,50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Obstacle(EnvironmentObject):
    """describing type of EnvironmentObject"""
    def __init__(self,x):
        """inherited, image, and rect attributes"""
        super().__init__(x)
        self.image = pygame.image.load('road_closed.png')
        self.image = pygame.transform.scale(self.image, (150,50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Player(pygame.sprite.Sprite):
    """user controlled player"""
    def __init__(self, x_pos, y_pos):
        """player attributes"""

        #inheriting sprite attributes
        super().__init__()

        #position attributes
        self.x = x_pos
        self.y = y_pos
        self.vx = 0.0
        self.vy = 0.0

        #image and rect attributes
        self.image = pygame.image.load('car.jpg')
        self.image = pygame.transform.scale(self.image, (50,80))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        #statistic attributes
        self.gas_level = 100
        self.score = 0
        self.gas_collected = 0
        self.obstacles_avoided = 0
        self.level = 1

        #alive flag
        self.alive = True

    def update(self):
        """updating player position by velocities given by controller"""
        #setting bounds on edge of screen
        if self.x < 1:
            if self.score > 9:
                self.x += 1.05*self.vx
            if self.score >19:
                self.x += 1.1*self.vx
            if self.score >34:
                self.x += 1.15*self.vx
            if self.score > 49:
                self.x += 1.2*self.vx
            if self.score >74:
                self.x += 1.25*self.vx
            if self.score > 99:
                self.x += 1.3*self.vx
            else:

                self.x = 1
                self.x += self.vx
        elif self.x > 589:
            if self.score > 9:
                self.x = 589
                self.x += 1.05*self.vx
            if self.score >19:
                self.x = 589
                self.x += 1.1*self.vx
            if self.score >34:
                self.x = 589
                self.x += 1.15*self.vx
            if self.score > 49:
                self.x = 589
                self.x += 1.2*self.vx
            if self.score >74:
                self.x = 589
                self.x += 1.25*self.vx
            if self.score > 99:
                self.x = 589
                self.x += 1.3*self.vx
            else:
                self.x = 589
                self.x += self.vx
        #update position
        else:
            if self.score > 9:
                self.x += 1.05*self.vx
            if self.score >19:
                self.x += 1.1*self.vx
            if self.score >34:
                self.x += 1.15*self.vx
            if self.score > 49:
                self.x += 1.2*self.vx
            if self.score >74:
                self.x += 1.25*self.vx
            if self.score > 99:
                self.x += 1.3*self.vx
            else:
                self.x += self.vx

        #setting bounds on edge of screen
        if self.y < 1:
            if self.score > 9:
                self.y += 1.05*self.vy
            if self.score >19:
                self.y += 1.1*self.vy
            if self.score >34:
                self.y += 1.15*self.vy
            if self.score > 49:
                self.y += 1.2*self.vy
            if self.score >74:
                self.y += 1.25*self.vy
            if self.score > 99:
                self.y += 1.3*self.vy
            else:
                self.y = 1
                self.y += self.vy
        elif self.y > 399:
            if self.score > 9:
                self.y = 399
                self.y += 1.05*self.vy
            if self.score >19:
                self.y = 399
                self.y += 1.1*self.vy
            if self.score >34:
                self.y = 399
                self.y += 1.15*self.vy
            if self.score > 49:
                self.y = 399
                self.y += 1.2*self.vy
            if self.score >74:
                self.y = 399
                self.y += 1.25*self.vy
            if self.score > 99:
                self.y = 399
                self.y += 1.3*self.vy
            else:
                self.y = 399
                self.y += self.vy
        #update position
        else:
            if self.score > 9:
                self.y += 1.05*self.vy
            if self.score >19:
                self.y += 1.1*self.vy
            if self.score >34:
                self.y += 1.15*self.vy
            if self.score > 49:
                self.y += 1.2*self.vy
            if self.score >74:
                self.y += 1.25*self.vy
            if self.score > 99:
                self.y += 1.3*self.vy
            else:
                self.y += self.vy

        #reduce gas slightly every cycle and kill player if it reaches 0
        self.gas_level -= .005
        if self.gas_level < 0:
            self.alive = False

        #updating rect position so collisions can be detected
        self.rect.y = self.y
        self.rect.x = self.x

        #updating level based on score
        if self.score > 10:
            self.level = 2
        if self.score > 20:
            self.level = 3
        if self.score > 35:
            self.level = 4
        if self.score > 50:
            self.level = 5

    def is_collided_with_gas(self, gas_group):
        """check each sprite in gas group for collision and modifying player if
        collision is detected"""
        for gas_sprite in gas_group:
            if self.rect.colliderect(gas_sprite.rect):
                #add to gas by hitting ped, update stat
                self.gas_level += 10
                self.gas_collected += 1
                #dont let gass get over 100
                if self.gas_level > 100:
                    self.gas_level = 100
                gas_sprite.kill()

    def is_collided_with_peds(self, ped_group):
        """check each sprite in ped group for collision and modifying player if
        collision is detected"""
        for ped_sprite in ped_group:
            if self.rect.colliderect(ped_sprite.rect):
                #add to score by hitting ped
                self.score += 1
                ped_sprite.kill()

    def is_collided_with_obst(self, obst_group):
        """check each sprite in obst group for collision and modifying player if
        collision is detected"""
        for obst_sprite in obst_group:
            if self.rect.colliderect(obst_sprite.rect):
                #kill player if it hits an obst
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
        #drawing the static road elements
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
            #pedestrian HUD
        myfont = pygame.font.SysFont('Arial', 20)
        textsurf = myfont.render('Score: '+str(self.model.player.score),
                                 False, (255,255,255))
        self.screen.blit(textsurf, (25,430))
        textsurf1 = myfont.render('Level: '+str(self.model.player.level),
                                  False, (255,255,255))
        self.screen.blit(textsurf1, (25, 410))
        self.screen.blit(self.hud_ped, (120,425))
            #gas HUD
        pygame.draw.rect(self.screen,
                         pygame.Color(255,0,0),
                         pygame.Rect(25,455,100,10))
        pygame.draw.rect(self.screen,
                         pygame.Color(0,255,0),
                         pygame.Rect(25,455,self.model.player.gas_level,10))
        self.screen.blit(self.hud_gas, (130,452.5))

        #drawing the player
        self.screen.blit(self.model.player.image, (self.model.player.x,self.model.player.y))

        pygame.display.update()

class Controller(object):
    """keyboard controls"""
    def __init__(self, model):
        """initialize model so player can be manipulated"""
        self.model = model

    def handle_event(self, event):
        """check for keydown events and change velocity in x and y directions"""
        pygame.key.set_repeat(1,50)
        #set velocities to 0 if no keys are pressed
        if event.type != KEYDOWN:
            self.model.player.vx = 0
            self.model.player.vy = 0
        #set velocities when keydown detected
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
    """Main menu"""
    #screen
    screen = pygame.display.set_mode((640,480))
    #screen.display.set_caption('ROAD RAGE')
    screen.fill(pygame.Color(255,0,0))

    #title display
    title_font = pygame.font.SysFont('Arial', 50)
    title_surf = title_font.render('ROAD RAGE', True, (0,0,0))

    #instruction display
    instruction_font = pygame.font.SysFont('Arial', 30)
    instruction_surf1 = instruction_font.render('The game is simple:',True,(0,0,0))
    instruction_surf2 = instruction_font.render('Avoid obstacles.',True,(0,0,0))
    instruction_surf3 = instruction_font.render('Hit pedestrians.',True,(0,0,0))
    instruction_surf4 = instruction_font.render('Dont run out of gas.',True,(0,0,0))
    instruction_surf5 = instruction_font.render('Use the arrow keys to move.',True,(0,0,0))
    instruction_surf6 = instruction_font.render('Press SPACE to start, or Esc to quit.',True,(0,0,0))

    #high score display
    high_scores = extract_high_scores(model)
    hs_font = pygame.font.SysFont('Arial', 20)
    hs_title = hs_font.render("Most Hit 'n Runs (so far)",True,(0,0,0))
    hs_1 = hs_font.render(str(high_scores[0]),True,(0,0,0))
    hs_2 = hs_font.render(str(high_scores[1]),True,(0,0,0))
    hs_3 = hs_font.render(str(high_scores[2]),True,(0,0,0))

    #menu loop with all of the information displayed
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
        #checks for space or escape clicks
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                #move to main loop if space is pressed
                if event.key == pygame.K_SPACE:
                    running = False
            if event.type == QUIT:
                sys.exit()
        pygame.display.update()

def death_screen(model):
    """screen that you see when you die"""

    #checking if the current score is high enough to be in the top 3
    store_high_scores(model)

    #screen
    screen = pygame.display.set_mode((640,480))
    screen.fill(pygame.Color(255,0,0))

    #death message
    msg_font = pygame.font.SysFont('Arial', 50)
    msg_surf = msg_font.render('YOU ARE DEAD', True, (0,0,0))

    #display game stats
    stat_font = pygame.font.SysFont('Arial', 30)
    stat_surf1 = stat_font.render('Pedestrians Hit: '+str(model.player.score),
                                   True, (0,0,0))
    stat_surf2 = stat_font.render('Gastanks Collected: '+str(model.player.gas_collected),
                                   True, (0,0,0))
    stat_surf3 = stat_font.render('Obstacles Avoided: '+str(model.player.obstacles_avoided),
                                   True, (0,0,0))
    stat_surf4 = stat_font.render('Level Reached: '+str(model.player.level),
                                   True, (0,0,0))

    #high score tag
    hs_font = pygame.font.SysFont('Arial', 15)
    high_score_surf = hs_font.render('***NEW HIGH SCORE***', True, (0,0,0))

    #instructions
    instruction_font = pygame.font.SysFont('Arial', 20)
    instruction_surf = instruction_font.render('Press SPACE to restart, press ESC to quit.',
                                   True, (0,0,0))

    #death screen loop that displays stats and instructions on how to proceed
    running = True
    while running:
        screen.blit(msg_surf, (150,100))
        screen.blit(stat_surf1, (150,150))
        screen.blit(stat_surf2, (150,180))
        screen.blit(stat_surf3, (150,210))
        screen.blit(stat_surf4, (150,240))
        screen.blit(instruction_surf, (150,400))
        #gives a high score tag if you get a high score
        if model.player.score in extract_high_scores(model):
            screen.blit(high_score_surf, (410, 155))
        #checking for events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #restart main program loop if space
                if event.key == K_SPACE:
                    return True
                if event.key == K_ESCAPE:
                    return sys.exit()
            if event.type == QUIT:
                sys.exit()
        pygame.display.update()

def main_game_loop(model,view,controller):
    """main game loop that checks for events, takes controller input,
    updates the model, and draws the model on the screen"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            controller.handle_event(event)
        model.update()
        #if the player dies it moves to the death screen
        if not model.player.alive:
            running = False
        view.draw()
        time.sleep(.001)

def store_high_scores(model):
    """stores top 3 local high scores"""
    filename = 'road_rage_high_scores.pickle'
    #load current top 3 scores
    current_scores = pickle.load(open(filename,'rb+'))
    #checks if current score is high enough to be a high score
    if model.player.score > min(current_scores):
        current_scores.pop()
        current_scores.append(model.player.score)
    #sorts the high scores and stores them again
    current_scores.sort(reverse=True)
    pickle.dump(current_scores,open(filename,'wb'))
    return

def extract_high_scores(model):
    """stores top 3 local high scores"""
    filename = 'road_rage_high_scores.pickle'
    #if no file exists puts in place holder high scores
    if not exists(filename):
        base_hs = [3,2,1]
        pickle.dump(base_hs,open(filename,'wb'))
    #returns the stored high score
    return pickle.load(open(filename, 'rb'))


if __name__ == "__main__":

    #initialize pygame modules
    pygame.init()
    pygame.font.init()
    pygame.display.init()
    pygame.display.set_caption('ROAD RAGE')

    #main program loop
    running = True
    while running:
        model = Model()
        view = View(model)
        controller = Controller(model)
        main_menu(model)
        main_game_loop(model,view,controller)
        running = death_screen(model)
