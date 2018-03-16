import pygame
from pygame.locals import *
import time
import random
import sys


class SnakeGameWindowView(object):
    """
    This class creates a window for the game.
    """
    def __init__(self, model, width, height):
        """
        This creates necessary model, screen and its width and height, and font.
        """
        self.model = model
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("arial", 50)
        self.width = width
        self.height = height
    def draw(self):
        """
        This function in the class will draw necessary materials
        and update every change in the window.
        """
        self.screen.fill(pygame.Color(0, 0, 0))
        for material in self.model.Mouse:
            pygame.draw.rect(self.screen,
                            pygame.Color(255, 0, 0),
                            pygame.Rect(material.x, material.y, material.height, material.width))
        for material in self.model.Snake:
            pygame.draw.rect(self.screen,
                            pygame.Color(0, 255, 0),
                            pygame.Rect(material.x, material.y, material.height, material.width), not material.head)
        for material in self.model.Arena:
            pygame.draw.rect(self.screen,
                            pygame.Color(0, 0, 255),
                            pygame.Rect(material.x, material.y, material.width, material.height),
                            material.padding)
        play_score = self.font.render(str(self.model.Score.score), 1, (125, 125, 0))
        text_rect = play_score.get_rect(center=(self.width/2, self.height/2))
        if self.model.Score.score == 'Game Over':
            self.screen.blit(play_score,text_rect)
            restart = self.font.render("Try again next time!", 1, (125, 125, 0))
            text_rect2 = restart.get_rect(center = (self.width/2, self.height*3/4))
            self.screen.blit(restart, text_rect2)
        else:
            self.screen.blit(play_score,(self.width - 100 , 50))
        pygame.display.update()

    def draw2(self):
        """
        This function draws the start screen of the game.
        """
        self.screen.fill(pygame.Color(0, 0, 0))
        welcome2 = self.font.render("Welcome to Snake Game!", 1, (125, 125, 0))
        welcome = self.font.render("Press Enter to Start", 1, (125, 125, 0))
        text_rect = welcome.get_rect(center=(self.width/2, self.height/2))
        text_rect2 = welcome2.get_rect(center = (self.width/2, self.height/4))
        self.screen.blit(welcome,text_rect)
        self.screen.blit(welcome2, text_rect2)
        pygame.display.update()


class SnakeGameModel(object):
    """
    This creates a model for this game.
    """
    def __init__(self):
        """This funciton will create dimensions for
        the blocks for the snake and the mouse."""
        self.Mouse = []
        self.Snake = []
        self.Arena = []
        snake = Snake(100, 10, 300, 300)
        self.Mouse.append(Mouse(10, 10, 100, 100))
        self.Arena.append(Arena())
        self.Score = Score()
        for i in range(snake.n):
            self.Snake.append(Snake(10, 10, i*snake.width+snake.x, snake.y, i == snake.n-1))
    def update(self):
        """
        This function will update the function.
        self.Snake[-1] represents the snake head
        """
        if self.Snake[-1].vx != 0  or self.Snake[-1].vy != 0:
            for i in range(len(self.Snake)-1):
                self.Snake[i].x = self.Snake[i+1].x
                self.Snake[i].y = self.Snake[i+1].y
        self.Snake[-1].update()

        if self.Snake[-1].x == self.Mouse[0].x and self.Snake[-1].y == self.Mouse[0].y:
            self.Mouse[0].x = random.randint(2,58) * 10
            self.Mouse[0].y = random.randint(2, 58) * 10
            self.Score.update()

            #Below is the snake growth logic
            if self.Snake[1].x - self.Snake[0].x == 10:
                self.Snake.insert(0, Snake(10, 10, self.Snake[0].x-10, self.Snake[0].y))
            if self.Snake[1].x - self.Snake[0].x == -10:
                self.Snake.insert(0, Snake(10, 10, self.Snake[0].x+10, self.Snake[0].y))
            if self.Snake[1].y - self.Snake[0].y == 10:
                self.Snake.insert(0, Snake(10, 10, self.Snake[0].x, self.Snake[0].y-10))
            if self.Snake[1].y - self.Snake[0].y == -10:
                self.Snake.insert(0, Snake(10, 10, self.Snake[0].x, self.Snake[0].y+10))

            print('The Snake gained length!')
            print("Score: " + str(self.Score))

        #Below is the snake collision logic
        if abs(self.Snake[-1].x - Arena().width) < Arena().padding or abs(self.Snake[-1].y - Arena().height) < Arena().padding:
            self.Snake[-1].vx = 0
            self.Snake[-1].vy = 0
            self.Score.update2()

        if self.Snake[-1].x < Arena().padding - 10 or self.Snake[-1].y < Arena().padding - 10:
            self.Snake[-1].vx = 0
            self.Snake[-1].vy = 0
            self.Score.update2()

        for i in range(len(self.Snake)-1):
            if self.Snake[i].x - self.Snake[-1].x == 0 and self.Snake[i].y - self.Snake[-1].y == 0:
                self.Snake[-1].vx = 0
                self.Snake[-1].vy = 0
                self.Score.update2()


    def __str__(self):
        output_lines = []
        for p in self.Mouse:
            output_lines.append(str(p))
        for p in self.Snake:
            output_lines.append(str(p))
        for p in self.Arena:
            output_lines.append(str(p))
        return "\n".join(output_lines)

class Arena(object):
    """
    Defines a boundary object to confine the snake

    Takes attributes height, width, padding
    padding refers to wall thickness
    """

    def __init__(self, width=600, height=600, padding = 20):
        self.height = height
        self.width = width
        self.x = 0
        self.y = 0
        self.padding = padding

    def __str__(self):
        return "The Boundary is %f by %f and is %f thick" % (self.height, self.width, self.padding)

class Mouse(object):

    def __init__(self, height, width, x, y):
        """
        This creates a mouse object.
        """
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __str__(self):
        return 'Mouse is in %f, %f' % (self.x, self.y)

class Snake(object):

    def __init__(self, height, width, x, y, h = False):
        """
        This creates a snake object with position, length, width, and velocity.
        If the segment represents the snakes head, self.head = 1
        """
        if h:
            self.head = 1
        else:
            self.head = 0

        self.height = height
        self.width = width
        self.n = int(height / width)
        self.x = x
        self.y = y
        self.vx = 10.0
        self.vy = 0.0

    def update(self):
        self.x += self.vx
        self.y += self.vy
    def __str__(self):
        return 'Snake is in %f, %f and is %f long.' % (self.x, self.y, self.height)

class Score(object):
    def __init__(self, score = 0):
        """
        This creates a score object that indicates the number of time it
        catches the mouse.
        """
        self.score = score
    def update(self):
        self.score  += 1
    def update2(self):
        """
        This specific update will happen when the snake collides with itself or
        the boundary.
        """
        self.score = 'Game Over'
    def __str__(self):
        return str(self.score)

class SnakeController(object):

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """
        This creates different operations for different keys in keyboard.
        """
        if event.type != KEYDOWN:
            return
        if self.model.Snake[-1].vy == 0 and self.model.Snake[-1].vx == 0:
            return
        if event.key == pygame.K_DOWN:
            if abs(self.model.Snake[-1].vy) != 0:
                return

            self.model.Snake[-1].vy = 10
            self.model.Snake[-1].vx = 0


        if event.key == pygame.K_LEFT:
            if abs(self.model.Snake[-1].vx) != 0:
                return

            self.model.Snake[-1].vy = 0
            self.model.Snake[-1].vx = -10

        if event.key == pygame.K_RIGHT:
            if abs(self.model.Snake[-1].vx) != 0:
                return

            self.model.Snake[-1].vy = 0
            self.model.Snake[-1].vx = 10

        if event.key == pygame.K_UP:
            if abs(self.model.Snake[-1].vy) != 0:
                return

            self.model.Snake[-1].vy = -10
            self.model.Snake[-1].vx = 0


    def handle_event2(self, event):
        """
        This creates keyboard operation specifically for the start screen.
        """
        if event.type != KEYDOWN:
            return

if __name__ == '__main__':
    def mainloop():
        pygame.init()
        pygame.display.set_caption('Snake Game')
        model = SnakeGameModel()
        window = SnakeGameWindowView(model, 600, 600)
        start = True
        run = False
        control = SnakeController(model)
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = True
                        start = False
                control.handle_event2(event)
            window.draw2()
            time.sleep(0.1)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                control.handle_event(event)
            model.update()
            window.draw()
            time.sleep(0.1)
    mainloop()
