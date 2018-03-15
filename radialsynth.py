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
import fluidsynth
from math import atan, pi

BLACK = (25, 25, 25)
GRAY = (40, 40, 40)
LTGRAY = (100, 100, 100)
YELLOW = (200, 200, 50)
RED = (160, 10, 10)
GREEN = (10, 160, 110)
BLUE = (60, 10, 160)


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
        self.buttons = {}
        button_size = (96,36)
        coord0 = (self.width*self.cell_size + 32, 0 + 36)
        self.buttons['R'] = Button(RED, self.screen, button_size, coordinates=coord0)
        self.buttons['G'] = Button(GREEN, self.screen, button_size, coordinates=tuple(map(sum, zip(coord0, (0,72)))))
        self.buttons['B'] = Button(BLUE, self.screen, button_size, coordinates=tuple(map(sum, zip(coord0, (0,144)))))
        self.buttons['Y'] = Button(YELLOW, self.screen, button_size, coordinates=tuple(map(sum, zip(coord0, (0,216)))))
        self.buttons['L'] = Button(LTGRAY, self.screen, button_size, coordinates=tuple(map(sum, zip(coord0, (0,288)))))
        self.buttons['S'] = Button(GRAY, self.screen, (72,72), coordinates=(self.width*self.cell_size + 44, 17*self.cell_size))
        self.buttons['C'] = Button(GRAY, self.screen, 36, pos=(self.width*self.cell_size + 80, 21*self.cell_size))

    def _draw_buttons(self):
        all_buttons = self.buttons.values()
        for button in all_buttons:
            button.draw()

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
        self._draw_buttons()
        pygame.display.update()

    def _add_block(self, mouse_pos, shape, color, d):
        coord = (mouse_pos[0]//36, mouse_pos[1]//36)
        self.blocks.pop(coord, None)
        block = Block(coord, self, shape, color, d)
        self.blocks[coord] = block

    def _remove_block(self, mouse_pos):
        coord = (mouse_pos[0]//36, mouse_pos[1]//36)
        self.blocks.pop(coord, None)

    def color_update(self):
        r, g, b = self.color_name
        d = self.d
        self.color = (r+d, g+d, b+d)

    def main_loop(self):
        """ Updates graphics and checks for pygame events """
        running = True
        shape = 'square'
        self.color_name = LTGRAY
        self.color = LTGRAY
        self.d = 40
        mode = 1
        while running:
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = 0
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    if mode > 0:
                        if event.button == 1 or event.button == 4:
                            self._add_block(event.pos, shape, self.color, self.d)
                        elif event.button == 3 or event.button == 5:
                            self._remove_block(event.pos)
                    else:
                        mode *= -1
                        s.make_rings(event.pos)
                        s.draw_rings()
                elif event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.d < 90:
                            self.d += 10
                        print(self.d)
                    elif event.key == pygame.K_DOWN:
                        if self.d > 30:
                            self.d -= 10
                        print(self.d)
                    elif event.key == pygame.K_r:
                        self.color_name = RED
                    elif event.key == pygame.K_g:
                        self.color_name = GREEN
                    elif event.key == pygame.K_b:
                        self.color_name = BLUE
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
                    self.color_update()
            time.sleep(.01)

class Block(object):
    """ A note block with attributes shape and color which determine the type
    of sound created when it is reached by the sweeper."""

    def __init__(self, cell_coordinates, world, shape, color, d):
        """ takes coordinates as a tuple """
        self.cell_coordinates = cell_coordinates
        self.world = world
        self.shape = shape
        self.color = color
        self.d = d

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

class Button():
    """ Creates a Button. """
    def __init__(self, color, draw_screen, dimensions, coordinates=None, pos=None):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.color = color
        self.pos = pos

    def draw(self):
        line_width = 0
        if self.pos == None:
            rect = pygame.Rect(self.coordinates, self.dimensions)
            pygame.draw.rect(self.draw_screen, self.color, rect, line_width)
        else:
            pygame.draw.circle(self.draw_screen, self.color, self.pos, self.dimensions, line_width)

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
        self.start = (start[0]//36, start[1]//36)
        print("start:", self.start)
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

    def pos_to_note(self, coord, offset):
        print(self.start, coord)
        if coord[1] == self.start[1]:
            if coord[0] >= self.start[0]:
                return 2 + offset
            else:
                return 6 + offset
        else:
            note = atan((coord[0]-self.start[0])/(coord[1]-self.start[1]))
            note = note*4/pi
            if coord[1] < self.start[1]:
                note += 4
            elif coord[0] < self.start[0]:
                note += 8
            return int(note + offset)

    def draw_rings(self):
        cells = self.world.cells
        screen = self.world.screen

        fs = fluidsynth.Synth()
        fs.start(driver="alsa")
        sfid = fs.sfload("example.sf2")
        fs.program_select(0, sfid, 0, 0)

        for ring in self.new_rings.values():
            short = []
            held = []
            for coord in ring:
                cell = cells[coord]
                coords = self.world._add_coords(cell.coordinates, (3, 3))
                rect_dim = (30, 30)
                image_rect = pygame.Rect(coords, rect_dim)
                pygame.draw.rect(screen, GRAY, image_rect, 0)
                if coord in self.world.blocks.keys():
                    d = self.world.blocks[coord].d
                    pitch = self.pos_to_note(coord, d)
                    color = self.world.blocks[coord].color
                    shape = self.world.blocks[coord].shape
                    if shape == 'circle':
                        short.append(pitch)
                    else:
                        held.append(pitch)
            for note in short:
                fs.noteon(0, note, 30)
            for note in held:
                fs.noteon(0, note, 30)
            pygame.display.update()
            time.sleep(.40)
            for note in short:
                fs.noteoff(0, note)
            self.world._redraw()
        for note in held:
            fs.noteoff(0, note)
        fs.delete()

if __name__ == "__main__":
    g = Grid()
    s = Sweeper(g)
    g.main_loop()
