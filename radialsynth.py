"""Created by Jane Sieving (jsieving) on 3/7/18.

Used code from AI & Algorithms Toolbox as base code for working with a grid-like
world in pygame.

This is the most recent working code for our radial synthesizer game. Currently
it can create a grid, draw and delete blocks on the grid, and change the block
type with user input. In progress is a Sweeper class which builds "rings" around
a chosen start square, reads all of the blocks in each ring, and plays sounds
depending on the blocks found, one ring at a time."""

import pygame
import time

BLACK = (25, 25, 25)
GRAY = (40, 40, 40)
LTGRAY = (100, 100, 100)
BLUE = (50, 100, 200)
RED = (200, 50, 100)
GREEN = (100, 200, 50)
YELLOW = (200, 200, 50)

class Grid():
    """ A grid full of cells, where note blocks can be placed by the user
    to 'draw' music."""

    def __init__(self, width=24, height=24, cell_size=36):
        pygame.init()
        screen_size = (width*cell_size + 160, height*cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ('RadialSynth')
        self.blocks = {}
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells()
        self._init_buttons()
        self.add_tile_type = None

    def _draw_background(self):
        self.screen.fill(BLACK)

    def _init_cells(self):
        self.cells = {}
        cell_size = (self.cell_size, self.cell_size)
        for i in range(self.height):
            for j in range(self.width):
                cell_coord = (i*self.cell_size, j*self.cell_size)
                self.cells[(i, j)] = Cell(self.screen, cell_coord, cell_size)

    def _add_coords(self, a, b):
        x = (a[0]+b[0])
        y = (a[1]+b[1])
        return (x, y)

    def _init_buttons(self):
        # TODO: draw buttons to the right of the grid to let the user
        # control the game without keyboard input.
        pass

    def _draw_cells(self):
        all_cells = self.cells.values()
        for cell in all_cells:
            cell.draw()

    def _draw_blocks(self):
        all_blocks = self.blocks.values()
        for block in all_blocks:
            block.draw()

    def _redraw(self):
        self._draw_background()
        self._draw_blocks()
        self._draw_cells()
        pygame.display.update()

    def _add_block(self, mouse_pos, shape, color):
        coord = (mouse_pos[0]//36, mouse_pos[1]//36)
        self.blocks.pop(coord, None)
        block = Block(coord, self, shape, color)
        self.blocks[coord] = block

    def _remove_block(self, mouse_pos):
        coord = (mouse_pos[0]//36, mouse_pos[1]//36)
        self.blocks.pop(coord, None)

    def main_loop(self):
        """ Updates graphics and checks for pygame events """
        running = True
        shape = 'square'
        color = LTGRAY
        mode = 1
        while running:
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = 0
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    if mode > 0:
                        if mouse
                        self._add_block(event.pos, shape, color)
                    else:
                        mode *= -1
                        print("Processing...")
                        s.make_rings(event.pos)
                        s.draw_rings()
                        print("Done.")
                elif event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        color = RED
                    elif event.key == pygame.K_g:
                        color = GREEN
                    elif event.key == pygame.K_b:
                        color = BLUE
                    elif event.key == pygame.K_c:
                        shape = 'circle'
                    elif event.key == pygame.K_s:
                        shape = 'square'
                    elif event.key == pygame.K_RETURN:
                        print(self.blocks)
                    elif event.key == pygame.K_DELETE:
                        self.blocks = {}
                    elif event.key == pygame.K_SPACE:
                        mode *= -1
                        print(mode)
            time.sleep(.01)

class Block(object):
    """ A note block with attributes shape and color which determine the type
    of sound created when it is reached by the sweeper."""

    def __init__(self, cell_coordinates, world, shape, color):
        """ takes coordinates as a tuple """
        self.cell_coordinates = cell_coordinates
        self.world = world
        self.shape = shape
        self.color = color

    def draw(self):
        cells = self.world.cells
        cell = cells[self.cell_coordinates]
        screen = self.world.screen
        if self.shape == 'square':
            coords = self.world._add_coords(cell.coordinates, (3, 3))
            rect_dim = (30, 30)
            self.image_rect = pygame.Rect(coords, rect_dim)
            pygame.draw.rect(screen, self.color, self.image_rect, 0)
        elif self.shape == 'circle':
            coords = self.world._add_coords(cell.coordinates, (18, 18))
            pygame.draw.circle(screen, self.color, coords, 16, 0)
        # screen.blit(self.image, self.image_rect)

class Cell():
    """ Spots in the grid where blocks can be drawn. """
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.color = GRAY

    def draw(self):
        line_width = 1
        rect = pygame.Rect(self.coordinates, self.dimensions)
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)

class Sweeper():
    """ Sweeps through the grid from an origin point, playing all the blocks
    in one 'ring' at a time."""
    def __init__(self, world):
        self.world = world
        self.rings = self.plan_rings(12)

    def overflow(self, a, b):
        x = (a[0]+b[0]) % 24
        y = (a[1]+b[1]) % 24
        return (x, y)

    def plan_rings(self, number):
        rings = {}
        for n in range(number):
            cells = []
            cells.extend([(n, y) for y in range(-n+1, n)])
            cells.extend([(-n, y) for y in range(-n, n)])
            cells.extend([(x, n) for x in range(-n, n)])
            cells.extend([(x, -n) for x in range(-n+1, n+1)])
            cells.append((n, n))
            rings[n] = cells
        return rings

    def make_rings(self, start):
        center = (start[0]//36, start[1]//36)
        new_rings = {}
        number = len(self.rings)
        for n in range(number):
            new_cells = []
            for coord in self.rings[n]:
                new_coord = self.overflow(center, coord)
                new_cells.append(new_coord)
            new_rings[n] = new_cells
        self.new_rings = new_rings

    def draw_rings(self):
        cells = self.world.cells
        screen = self.world.screen
        for ring in self.new_rings.values():
            for coord in ring:
                cell = cells[coord]
                coords = self.world._add_coords(cell.coordinates, (3, 3))
                print(coords)
                rect_dim = (30, 30)
                image_rect = pygame.Rect(coords, rect_dim)
                pygame.draw.rect(screen, GRAY, image_rect, 0)
            pygame.display.update()
            time.sleep(.33)
            self.world._redraw()
            print("Redrawn.")

if __name__ == "__main__":
    g = Grid()
    s = Sweeper(g)
    g.main_loop()
