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

    def _display_players(self):
        self.player1 = Player(self.screen,10,350,240,(255,140,0))
        self.player2 = Player(self.screen,10,290,240,(255,140,0))
        self.player1.draw
        self.player2.draw

    def _redraw(self):
        self._draw_background()
        self._draw_cells()
        self._display_players()
        pygame.display.update()

    def main_loop(self):
        running = True
        while running:
            self._redraw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    controller = KeyControl(self.player1,self.player2)
                    controller.handle_event

class Cell(object):
    def __init__(self, draw_screen, coordinates, side_length):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.side_length = side_length
        self.color = (0, 0, 0)

    def draw(self):
        line_width = 1
        rect = pygame.Rect(self.coordinates, self.side_length)
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)

class Player(object):
    def __init__(self, draw_screen, dimension, start_posx, start_posy, color=(255,255,255)):
        self.draw_screen = draw_screen
        self.width = dimension
        self.height = dimension
        self.x = start_posx
        self.y = start_posy
        self.dir = "r"
        self.vx = .2
        self.color = color

    def draw(self):
        line_width = .5
        pygame.draw.rect(self.draw_screen,self.color,pygame.Rect(self.x,self.y,self.width,self.height))

    def update(self):
        if self.dir == "r":
            self.x += self.vx
        elif self.dir == "l":
            self.x += -self.x
        elif self.dir == "u":
            self.y += self.vx
        elif self.dir == "d":
            self.y += -self.vx

class KeyControl(object):
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def handle_event(self, event):
        if event == K_LEFT:
            if self.player1.dir == "r":
                return
            self.player1.dir = "l"
        if event == K_RIGHT:
            if self.player1.dir == "l":
                return
            self.player1.dir = "r"
        if event == K_DOWN:
            if self.player1.dir == "u":
                return
            self.player1.dir = "d"
        if event == K_UP:
            if self.player1.dir == "d":
                return
            self.player1.dir = "u"

        if event == K_a:
            if self.player2.dir == "r":
                return
            self.player2.dir = "l"
        if event == K_d:
            if self.player2.dir == "l":
                return
            self.player2.dir = "r"
        if event == K_s:
            if self.player2.dir == "u":
                return
            self.player2.dir = "d"
        if event == K_w:
            if self.player2.dir == "d":
                return
            self.player2.dir = "u"


if __name__ == '__main__':
    world = TronWorld()
    world.main_loop()
