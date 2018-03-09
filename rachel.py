#THIS FILE IS DOPE
import pygame
from pygame.locals import *
import time


class Penguin(pygame.sprite.Sprite): # code is from pygame documenta
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
       # Call the parent class (Sprite) constructor
       super().__init__()

       # Create an image of the block, and fill it with a color.
    #   self.image = pygame.Surface([width, height])
     #  self.image.fill('BLACK')
       # self.image = pygame.image.load("/path/to/image_file.png") -- use to import image

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.image = pygame.image.load("penguin_smol.png").convert()
       self.rect = self.image.get_rect()
    pass

class Cell():
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.color = (0, 0, 0)

    def draw(self):
        line_width = 1  # SPACE BETWEEN CELLS
        rect = pygame.Rect(self.coordinates, self.dimensions)
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)

class Track_View(object): # code taken from AI toolbox, naomi used it too
    def __init__(self, width=15, height=10, cell_size=30):          # width and height are number of cells and are switched
        pygame.init()
        screen_size = (height * cell_size, width * cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ('Paul World')
        #self.actors = {}
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells()

    def _draw_background(self):
        WHITE = (255, 255, 255)
        self.screen.fill(WHITE)

    def _init_cells(self):
        self.cells = {}
        cell_size = (self.cell_size, self.cell_size)
        for i in range(self.height):
            for j in range(self.width):
                cell_coord = (i * self.cell_size, j * self.cell_size)
                self.cells[(i, j)] = Cell(self.screen, cell_coord, cell_size)

    def _draw_cells(self):
        all_cells = self.cells.values()
        for cell in all_cells:
            cell.draw()

    def _redraw(self):
        self._draw_background()
        #self._draw_actors()
        self._draw_cells()
        pygame.display.update()
    pass

    def main_loop(self): #lots of extra functions, have to clean up but we can use the keydown stuff
        """Update graphics and check for pygame events."""
        running = True
        SCREENWIDTH= 400
        SCREENHEIGHT=500
        WHITE = (255, 0, 0)
        size = (SCREENWIDTH, SCREENHEIGHT)
        screen = pygame.display.set_mode(size)
        all_penguins = pygame.sprite.Group()
        penguin = Penguin()
        penguin.rect.x = 15
        penguin.rect.y = 15
        all_penguins.add(penguin)
        while running:
            #self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False

            all_penguins.update()
            screen.fill(WHITE)
            all_penguins.draw(screen)

                # elif event.type is pygame.MOUSEBUTTONDOWN:
                #     pass
                #     # if self.add_tile_type == 'lava':
                #     #     self._add_lava(event.pos)
                #     # insert swamp code here
                # elif event.type is pygame.KEYDOWN:
                #     pass
                #     # if event.key == pygame.K_SPACE:
                #     #     self.paul.run_astar(self.cake.cell_coordinates, self)
                #     #     self.paul.get_path()


        pygame.quit()
class Obstacles(object):
    pass


class Sled_model(object):
    pass


class CPSled_main:
    pass

if __name__ == '__main__':
    world = Track_View()
    world.main_loop()
    pygame.quit()
    # pygame.init()
    #
    # size = (1024, 768)
    # screen = pygame.display.set_mode(size)
    #
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             running = False
    #     time.sleep(.001)
    #
    # pygame.quit()
