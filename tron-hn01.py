"Naomi's Working Space"
import pygame
from pygame.locals import*
import time

class PyGameWindowView(object):
    def __init__(self,model,width=640,height=480):
        self.model = model
        size = (width,height)
        self.model.screen = pygame.display.set_mode(size)

    def _init_draw(self):
        self.model.screen.fill((105,105,105))
        self.model.cells = {}
        cell_size = (self.model.cell_length, self.model.cell_length)
        for i in range(self.model.height):
            for j in range(self.model.width):
                cell_coord = (i*self.model.cell_length,j*self.model.cell_length)
                self.model.cells[(i,j)] = Cellview(self.model.screen,cell_coord,cell_size)
        all_cells = self.model.cells.values()

        for cell in all_cells:
            cell.draw()

    def draw(self):
        self.model._draw_players()
        pygame.display.update()

class TronModelView(object):
    def __init__(self,cell_length=10,width=640,height=480):
        pygame.init()
        size = (width,height)
        self.screen = pygame.display.set_mode(size)
        self.width = width
        self.height = height
        self.cell_length = cell_length
        self.cell_lst = []
        self.player_paths = []
        self.player1 = Player(self.screen,10,(self.width/2+100),(self.height/2),"r",(255,140,0))
        self.player2 = Player(self.screen,10,(self.width/2-100),(self.height/2),"l",(0,255,0))
        self.cells_loc = {}
        for i in range(self.height//cell_length):
            for j in range(self.width//cell_length):
                cell_coords = (i*self.cell_length, j*self.cell_length)
                self.cell_lst.append(Cell(cell_coords, cell_length))





    def in_cell(self):
        for cell in self.cell_lst:
            if self.player1.x in cell.xrange and self.player1.y in cell.yrange:
                self.player1.current_cell = cell
                break

        for cell in self.cell_lst:
            if self.player2.x in cell.xrange and self.player2.y in cell.yrange:
                self.player2.current_cell = cell
                break

    def _draw_players(self):
        self.player1.draw()
        self.player2.draw()

    def update(self):
        self.player1.update()
        self.player2.update()
        if self.player1.crash():
            self.end_game("PLAYER 2 ")
            self.player1.dir = "None"
            self.player2.dir = "None"
        if self.player2.crash():
            self.end_game("PLAYER 1 ")
            self.player1.dir = "None"
            self.player2.dir = "None"

        """last_seen_p1 = self.player1.current_cell
        last_seen_p2 = self.player2.current_cell
        self.in_cell()
        if self.player1.current_cell != last_seen_p1:
            self.player_paths.append(last_seen_p1)

        if self.player2.current_cell != last_seen_p2:
            self.player_paths.append(last_seen_p2)"""


        if self.player1.current_cell in self.player_paths:
            self.end_game("PLAYER 2 ")
            self.player1.dir = "None"
            self.player2.dir = "None"
        if self.player2.current_cell in self.player_paths:
            self.end_game("PLAYER 1 ")
            self.player1.dir = "None"
            self.player2.dir = "None"


    def end_game(self,player):
        pygame.display.set_caption(player + "WINS!")


class Cell(object):
    def __init__(self,coords, cell_length):
        self.xmin = coords[0]
        self.ymin = coords[1]
        self.xmax = coords[0] + cell_length
        self.ymax = coords[1] + cell_length
        self.xrange = range(self.xmin, self.xmax)
        self.yrange = range(self.ymin, self.ymax)

class Cellview(object):
    def __init__(self, draw_screen, coordinates, cell_length):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.side_length = cell_length
        self.color = (0, 0, 0)

    def draw(self):
        line_width = 1
        rect = pygame.Rect(self.coordinates, self.side_length)
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)

class Player(object):
    def __init__(self, draw_screen, dimension, start_posx, start_posy, direction, color=(255,255,255)):
        self.draw_screen = draw_screen
        self.width = dimension
        self.height = dimension
        self.x = start_posx
        self.y = start_posy
        self.vx = 0
        self.vy = 0
        self.dir = direction
        self.color = color
        self.current_cell = None



    def draw(self):
        line_width = .5
        pygame.draw.rect(self.draw_screen,self.color,pygame.Rect(self.x,self.y,self.width,self.height))

    def update(self):
        if self.dir == "r":
            self.vx = 10
            self.vy = 0
        elif self.dir == "l":
            self.vx = -10
            self.vy = 0
        elif self.dir == "u":
            self.vx = 0
            self.vy = -10
        elif self.dir == "d":
            self.vx = 0
            self.vy = 10
        elif self.dir == "None":
            self.vx = 0
            self.vy = 0
        self.x += self.vx
        self.y += self.vy


    def crash(self):
        if self.x == 640 or self.x == -10:
            return True
        if self.y == -10 or self.y == 480:
            return True
        return False

class PlayerPath(object):
    def __init__(self,model):
        self.model = model
        self.model.cells_loc = {}
        for i in range(self.model.height):
            for j in range(self.model.width):
                cell_coords = (i*self.model.cell_length,j*self.model.cell_length)
                self.model.cells_loc[(i,j)] = Cell(self.model.screen,cell_coords,cell_size)

        self.model.hit_cells = [(self.model.player1.x, self.model.player1.y), (self.model.player2.x, self.model.player2.y)]

    def update(self):
        if (self.model.player1.x, self.model.player1.y) not in self.hit_cells:
            self.hit_cells.append((player1.x, player1.y))
        if (self.model.player2.x, self.model.player2.y) not in self.hit_cells:
            self.hit_cells.append




class KeyControl(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            if self.model.player1.dir != "r":
                self.model.player1.dir = "l"
        if event.key == pygame.K_RIGHT:
            if self.model.player1.dir != "l":
                self.model.player1.dir = "r"
        if event.key == pygame.K_DOWN:
            if self.model.player1.dir != "u":
                self.model.player1.dir = "d"
        if event.key == pygame.K_UP:
            if self.model.player1.dir != "d":
                self.model.player1.dir = "u"

        if event.key ==pygame.K_a:
            if self.model.player2.dir != "r":
                self.model.player2.dir = "l"
        if event.key == pygame.K_d:
            if self.model.player2.dir != "l":
                self.model.player2.dir = "r"
        if event.key == pygame.K_s:
            if self.model.player2.dir != "u":
                self.model.player2.dir = "d"
        if event.key == pygame.K_w:
            if self.model.player2.dir != "d":
                self.model.player2.dir = "u"


if __name__ == '__main__':
    pygame.init()
    model = TronModelView()
    view = PyGameWindowView(model)
    view._init_draw()
    controller = KeyControl(model)

    running = True
    while running:
        view._init_draw
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.2)

    pygame.quit()
