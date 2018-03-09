import pygame
from pygame.locals import *
import time


class SnakeGameWindowView(object):

    def __init__(self, model, width, height):
        self.model = model
        self.screen = pygame.display.set_mode((width, height))
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
                            pygame.Rect(material.x, material.y, material.height, material.width))
        for material in self.model.Arena:
            pygame.draw.rect(self.screen,
                            pygame.Color(0, 0, 255),
                            pygame.Rect(material.x, material.y, material.width, material.height),
                            material.padding)
        pygame.display.update()

class SnakeGameModel(object):

    def __init__(self):
        """This funciton will create dimensions for
        the blocks for the snake and the mouse."""
        self.Mouse = []
        self.Snake = []
        self.Arena = []
        snake = Snake(100, 10, 300, 300)
        self.Mouse.append(Mouse(10, 10, 100, 100))
        self.Arena.append(Arena())
        for i in range(int(snake.height / snake.width)):
            self.Snake.append(Snake(snake.height / snake.width, 10, i*snake.width+snake.x, snake.y))
    def update(self):
        """
        This function will update the function.
        """
        for part in self.Snake:
            part.update()
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

    def __init__(self, width=640, height=800, padding = 20):
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

    def __init__(self, height, width, x, y):
        """
        This creates a snake object with position, length, width, and velocity.
        """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        self.x += self.vx
        self.y += self.vy
    def __str__(self):
        return 'Snake is in %f, %f and is %f long.' % (self.x, self.y, self.height)

class SnakeController(object):

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """
        This creates different operations for different keys in keyboard.
        """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_DOWN:
            if abs(self.model.Snake[-1].vy) == -.1:
                return
            #if self.model.Snake[-1].vx == -.1:
            #    self.model.Snake.reverse()
            while self.model.Snake[0].x != self.model.Snake[-1].x:
                for i in range(len(self.model.Snake)-1):
                    self.model.Snake[i].x += self.model.Snake[i+1].x - self.model.Snake[i].x
                    self.model.Snake[i].y += self.model.Snake[i+1].y - self.model.Snake[i].y
                    if self.model.Snake[i].x == self.model.Snake[-1].x:
                        self.model.Snake[i].y += self.model.Snake[i].width

            if self.model.Snake[0].x == self.model.Snake[-1].x:
                for part in self.model.Snake:
                    part.vy = .1
                    part.vx = 0


        if event.key == pygame.K_LEFT:
            if abs(self.model.Snake[-1].vx) == -.1:
                return
            #if self.model.Snake[-1].vy == .1:
            #    self.model.Snake.reverse()
            while self.model.Snake[0].y != self.model.Snake[-1].y:
                for i in range(len(self.model.Snake)-1):
                    self.model.Snake[i].x += self.model.Snake[i+1].x - self.model.Snake[i].x
                    self.model.Snake[i].y += self.model.Snake[i+1].y - self.model.Snake[i].y
                    if self.model.Snake[i].y == self.model.Snake[-1].y:
                        self.model.Snake[i].x -= self.model.Snake[i].width

            if self.model.Snake[0].y == self.model.Snake[-1].y:
                for part in self.model.Snake:
                    part.vy = 0
                    part.vx = -.1

        if event.key == pygame.K_RIGHT:
            if abs(self.model.Snake[-1].vx) == -.1:
                return
            #if self.model.Snake[-1].vy == -.1:
            #    self.model.Snake.reverse()
            while self.model.Snake[0].y != self.model.Snake[-1].y:
                for i in range(len(self.model.Snake)-1):
                    self.model.Snake[i].x += self.model.Snake[i+1].x - self.model.Snake[i].x
                    self.model.Snake[i].y += self.model.Snake[i+1].y - self.model.Snake[i].y
                    if self.model.Snake[i].y == self.model.Snake[-1].y:
                        self.model.Snake[i].x += self.model.Snake[i].width

            if self.model.Snake[0].y == self.model.Snake[-1].y:
                for part in self.model.Snake:
                    part.vy = 0
                    part.vx = .1

        if event.key == pygame.K_UP:
            if abs(self.model.Snake[-1].vy) == -.1:
                return
            #if self.model.Snake[-1].vx == -.1:
            #    self.model.Snake.reverse()
            while self.model.Snake[0].x != self.model.Snake[-1].x:
                for i in range(len(self.model.Snake)-1):
                    self.model.Snake[i].x += self.model.Snake[i+1].x - self.model.Snake[i].x
                    self.model.Snake[i].y += self.model.Snake[i+1].y - self.model.Snake[i].y
                    if self.model.Snake[i].x == self.model.Snake[-1].x:
                        self.model.Snake[i].y -= self.model.Snake[i].width

            if self.model.Snake[0].x == self.model.Snake[-1].x:
                for part in self.model.Snake:
                    part.vx = 0
                    part.vy = -.1

if __name__ == '__main__':
    pygame.init()
    model = SnakeGameModel()
    window = SnakeGameWindowView(model, 640, 800)
    run = True
    control = SnakeController(model)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            control.handle_event(event)
        model.update()
        window.draw()
        time.sleep(0.001)
    pygame.quit()
