"""

"""
#TODO: add different fruits, add gravity, add mouse controller, add collision detection


import pygame
from pygame.locals import *
import time

class PyGameWindowView(object):
    """ A view of fruit ninja rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        for fruit in self.model.fruits:
            pygame.draw.rect(self.screen,
                             pygame.Color(255, 255, 255),
                             pygame.Rect(fruit.x,
                                         fruit.y,
                                         fruit.width,
                                         fruit.height))
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         pygame.Rect(self.model.blade.x,
                                     self.model.blade.y,
                                     self.model.blade.width,
                                     self.model.blade.height))

        pygame.display.update()



class FruitNinjaModel(object):
    """ Encodes a model of the game state """
    def __init__(self):
        self.fruits = []
        self.fruits.append(Fruit(20, 20, 10, 10))
        self.blade = Blade(20, 100, 200, 30)

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        for fruit in self.fruits:
            output_lines.append(str(fruit))
        # print one fruit per line
        return "\n".join(output_lines)



    def update(self):
        """ Update the game state (currently only tracking the blade) """
        self.blade.update()









class Fruit(object):
    """ Encodes the state of a fruit in the game """
    def __init__(self,height,width,x,y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __str__(self):
        return "Fruit height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)


class Blade(object):
    """ Encodes the state of the Blade in the game """
    def __init__(self, height, width, x, y):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0

    def update(self):
        """ update the state of the paddle """
        self.x += self.vx

    def __str__(self):
        return "Blade height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                           self.y)
class PyGameMouseController(object):
    """ A controller that uses the mouse to move the paddle """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Handle the mouse event so the paddle tracks the mouse position """
        if event.type == MOUSEMOTION:
            self.model.blade.x = event.pos[0] - self.model.blade.width/2.0
            self.model.blade.x = event.pos[0] - self.model.blade.height/2.0

if __name__ == '__main__':
    pygame.init()

    size = (640, 480)

    model = FruitNinjaModel(size)
    print(model)
    view = PyGameWindowView(model, size)
    controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
