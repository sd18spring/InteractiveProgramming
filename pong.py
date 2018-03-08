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
                        pygame.Rect(self.model.paddle.x,
                                    self.model.paddle.y,
                                    self.model.paddle.width,
                                    self.model.paddle.height))
        pygame.display.update()


class PongModel(object):
    """Encodes a model of the game state"""

    def ___init(self,size):
        self.width = size[0]
        self.height = size[1]
        self.paddle = Paddle(100, 20, self.width, self.height / 2)


    def update(self):

        self.paddle.update()


    def __str__(self):
        output_lines = []

        output_lines.append(str(self.paddle))

        return "\n".join(output_lines)





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

    def handle_envent(self, event):

        if event.key == MOUSEMOTION:
            self.model.paddle.x = event.pos(0) - self.model.paddle.width/2.0



if __name__ == '__main__':
    pygame.init()

    size = (1800, 1000)
    model = PongModel(size)

    view = PyGameWindowView(model, size)

    controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                 running = False
            controller.handle_event(event)
        model.update()
        view.draw
        time.sleep(.001)

    pygame.quit()
