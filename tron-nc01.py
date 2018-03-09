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
                self.model.cells[(i,j)] = Cell(self.model.screen,cell_coord,cell_size)
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
        self.player1 = Player(self.screen,10,(self.width/2+100),(self.height/2),"r",(255,140,0))
        self.player2 = Player(self.screen,10,(self.width/2-100),(self.height/2),"l",(0,255,0))

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

    def end_game(self,player):
        pygame.display.set_caption(player + "WINS!")

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
        time.sleep(.1)

    pygame.quit()
