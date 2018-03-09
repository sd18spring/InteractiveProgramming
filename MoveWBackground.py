import pygame
from pygame.locals import *
import time
pygame.init()
#display.set_mode(resolution=(0,0), flags=0, depth=0)
background_image = pygame.image.load("GrassBackground.jpg").convert()
class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, size=(800, 600)):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(resolution=(800,600))
        self.screen.blit(background_image, [0, 0])

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        # for brick in self.model.bricks:
        #     pygame.draw.rect(self.screen,
        #                      pygame.Color(255, 255, 255),
        #                      pygame.Rect(brick.x,
        #                                  brick.y,
        #                                  brick.width,
        #                                  brick.height))
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         pygame.Rect(self.model.paddle.x,
                                     self.model.paddle.y,
                                     self.model.paddle.width,
                                     self.model.paddle.height))
        pygame.display.update()



class BrickBreakerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.bricks = []
        self.width = size[0]
        self.height = size[1]
        self.brick_width = 100
        self.brick_height = 40
        self.brick_space = 10

        self.paddle = Paddle(20, 100, 500, self.height - 500)

    def update(self):
        """ Update the game state (currently only tracking the paddle) """
        self.paddle.update()

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        for brick in self.bricks:
            output_lines.append(str(brick))
        output_lines.append(str(self.paddle))
        # print one item per line
        return "\n".join(output_lines)


class Paddle(object):
    """ Encodes the state of the paddle in the game """
    def __init__(self, height, width, x, y):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        """ update the state of the paddle """
        self.x += self.vx
        self.y += self.vy
    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                           self.y)
class PyGameKeyboardController(object):
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the paddle """
        #link for event.key https://www.pygame.org/docs/ref/key.html
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.x += -1
        if event.key == pygame.K_RIGHT:
            self.model.paddle.x += 1
        if event.key == pygame.K_UP:
            self.model.paddle.y += -1
        if event.key == pygame.K_DOWN:
            self.model.paddle.y += 1

if __name__ == '__main__':
    pygame.init()

    size = (1000, 1000)

    model = BrickBreakerModel(size)
    print(model)
    view = PyGameWindowView(model, size)
    #controller = PyGameKeyboardController(model)
    controller = PyGameKeyboardController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
