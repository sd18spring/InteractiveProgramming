import pygame
from pygame.locals import *
import time
from random import randint


class WindowView:
    def __init__(self, model, size):
        '''Initialize the view with a reference to the model and
        screen dimensions (width, height)
        '''
        self.model = model
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont('dejavu', 45)

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))

        for i, rect in enumerate(self.model.pipe.rects()[3]):
            pygame.draw.rect(self.screen,
                             pygame.Color(255, 255, 255),
                             rect,
                             2)
            self.screen.blit(self.font.render(str(self.model.pipe.prob.choices[i]), True, (255,255,255)), (rect.left + 5, rect.top + self.size[1] / 8 - 10))

        if self.model.pipe.x <= 0 - self.model.pipe.width:
            self.model.pipe.prob.new_prob()
            self.model.pipe.vx += 0.1

        self.screen.blit(self.font.render(
            self.model.pipe.prob.display_prob(), True, (0, 0, 255)), (50, 20))

        self.screen.blit(self.font.render(
            str(self.model.pipe.score), True, (255, 255, 0)), (500, 20))

        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         self.model.nerd.rect())

        if self.model.game_over:
            self.screen.blit(self.font.render(
                self.model.over_message, True, (0, 255, 255)), (100, 200))
        pygame.display.update()


class Model:
    '''Holds the model of the game state'''

    def __init__(self, size):
        self.nerd = Nerd()
        self.pipe = Pipe()
        self.game_over = False
        self.over_message = "Game Over, Press Enter"

    def update(self):
        if not self.game_over:
            self.nerd.update()
            self.pipe.update()

        if self.nerd.rect().colliderect(self.pipe.rects()[1]) or self.nerd.rect().colliderect(self.pipe.rects()[0]):
            self.game_over = True

    def reset(self):
        self.pipe = Pipe()
        self.game_over = False


class Nerd:
    ''' The state of the nerd '''

    def __init__(self, x=40, y=100, width=40, height=40, floor=480):
        self.height = height
        self.width = width
        self.floor = floor
        self.x = x
        self.y = y
        self.vy = 0
        self.g = 1/9

    def update(self):
        if self.y < 0:
            self.y = 0
        elif self.y >= self.floor:
            self.y = self.floor - self.height
        else:
            self.y += self.vy
        self.vy = 10/3 if self.vy > 10/3 else self.vy + self.g

    def rect(self):
        return pygame.Rect(self.x,
                           self.y,
                           self.width,
                           self.height)


class KeyboardController:
    ''' Handles keyboard input for flappy nerd '''

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Space sets the nerd's velocity. """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_SPACE:
            self.model.nerd.vy = -10/3
        if event.key == pygame.K_RETURN:
            self.model.game_over = self.model.reset()


class Pipe:
    def __init__(self, x=640, width=80, height=480, valid=0, vx=2/3, max_x=640, floor=480):
        self.width = width
        self.vx = vx
        self.x = x
        self.max_x = x
        self.safe_lvl = randint(0, 3)
        self.height = height
        self.score = 0
        self.prob = MultProb(safe_lvl=self.safe_lvl)

    def update(self):
        if self.x < -self.width:
            self.x = self.max_x
            self.score += 1
            self.safe_lvl = randint(0, 3)
            self.prob = MultProb(safe_lvl=self.safe_lvl)
        else:
            self.x -= self.vx

    def rects(self):
        top = pygame.Rect(self.x,
                          0,
                          self.width,
                          self.height / 4 * self.safe_lvl)

        bottom = pygame.Rect(self.x,
                             self.height / 4 * (self.safe_lvl + 1),
                             self.width,
                             self.height)

        safe = pygame.Rect(self.x,
                           self.height / 4 * self.safe_lvl,
                           self.width,
                           self.height / 4)

        text_blocks = [pygame.Rect(
            self.x, self.height / 4 * y, self.width, self.height / 4) for y in range(4)]

        return top, bottom, safe, text_blocks


class MultProb:
    def __init__(self, safe_lvl, nchoices=4):
        self.nchoices = nchoices
        self.safe_lvl = safe_lvl
        self.new_prob()
        self.ans = self.a * self.b
        self.generate_choices()

    def generate_choices(self):
        choices = []
        for x in range(self.nchoices - 1):
            choice = self.ans
            while choice == self.ans:
                choice = randint(self.a // 10 * self.b // 10 * 100, (self.a // 10 + 1)
                                 * (self.b // 10 + 1) * 100) // 10 * 10 + self.ans % 10
            choices.append(choice)
        choices.insert(self.safe_lvl, self.ans)
        self.choices = choices

    def new_prob(self):
        self.a = randint(0, 100)
        self.b = randint(0, 100)
        self.ans = self.a * self.b
        self.generate_choices()

    def display_prob(self):
        return str(self.a) + " x " + str(self.b)

if __name__=='__main__':
    pygame.init()
    size = (640, 480)
    model = Model(size)
    view = WindowView(model, size)
    running = True
    controller = KeyboardController(model)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.01)
    pygame.quit()
