"Naomi's Working Space"
import pygame
from pygame.locals import*

class TronWorld():
    def __init__(self,cell_length=10,width=640,height=480):
        pygame.init()
        size = (width,height)
        self.screen = pygame.display.set_mode(size)
        self.width = width
        self.height = height
        self.cell_length = cell_length
        self._init_cells()

    def _init_cells(self):
        self.cells = {}
        cell_size = (self.cell_length, self.cell_length)
        for i in range(self.height):
            for j in range(self.width):
                cell_coord = (i * self.cell_length, j*self.cell_length)
                self.cells[(i,j)] = Cell(self.screen, cell_coord, cell_size)

    def _draw_background(self):
        gray = (105, 105, 105)
        self.screen.fill(gray)

    def _draw_cells(self):
        all_cells = self.cells.values()
        for cell in all_cells:
            cell.draw()

    def _redraw(self):
        self._draw_background()
        self._draw_cells()
        pygame.display.update()

    def main_loop(self):
        running = True
        while running:
            self._redraw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

class Cell(object):
    def __init__(self, draw_screen, coordinates, side_length, color=(0,0,0)):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.side_length = side_length
        self.color = color

    def draw(self):
        line_width = 1
        rect = pygame.Rect(self.coordinates, self.side_length)
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)


if __name__ == '__main__':
    world = TronWorld()
    world.main_loop()
