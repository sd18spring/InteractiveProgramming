import pygame
from pygame.locals import *
import time

class PyGameWindowView(object):
    """ A view of the Pong game rendered in a PyGame Window"""
    def __init__(self, model, size):
        """ Initialize the PyGame window of the game """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """Draw the current game state to the screen"""
        self.screen.fill(pygame.Color(135, 206, 250))
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 127, 80),
                        pygame.Rect(self.model.paddle1.x,
                                    self.model.paddle1.y,
                                    self.model.paddle1.width,
                                    self.model.paddle1.height))
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 127, 80),
                        pygame.Rect(self.model.paddle2.x,
                                    self.model.paddle2.y,
                                    self.model.paddle2.width,
                                    self.model.paddle2.height))

        pygame.draw.circle(self.screen,
                           pygame.Color(255,255,102),
                           (self.model.ball.x,
                           self.model.ball.y),
                           self.model.ball.radius)

        pygame.display.update()


class PongModel(object):
    """Encodes a model of the game state"""

    def __init__(self,size):
        self.width = size[0]
        self.height = size[1]
        self.paddle1 = Paddle(100, 20, 10, self.height)
        self.paddle2 = Paddle(100, 20, self.width - 30, self.height / 2)
        self.ball = Ball(self.width/2, self.height/2, 10)


    def update(self):

        self.paddle1.update()
        self.paddle2.update()

    def __str__(self):
        output_lines = []

        output_lines.append(str(self.paddle1))
        output_lines.append(str(self.paddle2))


        return "\n".join(output_lines)

class Ball(object):

    def __init__(self, x, y, radius):

        self.x = x
        self.y = y
        self.radius = radius
        self.vy = 0.0
        self.vx = 0.0


    def update(self):

        self.y += self.vy
        self.x += self.vx




    def __str__(self):
        return "Ball x=%f, y=%f, radius=%f" % (self.x, self.y, self.radius)



class Paddle(object):
    """Encodes the state of the paddle 1 in the game"""

    def __init__(self, height, width, x, y):
        """Initalize a paddle with the sepcified height, width, and position (x,y) """

        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = 0.0

    def update(self):
        """update the state of the paddle"""

        self.y += self.vy

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height, self.width, self.x, self.y)


class PyGameMouseController(object):

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.model.paddle1.y = event.pos[1] - self.model.paddle1.height/2.0


class PyGameKeyboardController(object):

    def __init__(self,event):
        self.model = model

    def handle_event(self,event):

        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.paddle2.vy += -1.0
        if event.key == pygame.K_DOWN:
            self.model.paddle2.vy += 1.0



if __name__ == '__main__':
    pygame.init()

    size = (1800, 800)
    model = PongModel(size)

    view = PyGameWindowView(model, size)

    controller1 = PyGameMouseController(model)
    controller2 = PyGameKeyboardController(model)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                 running = False
            controller1.handle_event(event)
            controller2.handle_event(event)

        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
