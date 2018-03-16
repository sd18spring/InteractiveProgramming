"""
Master Copy
Tron Remake

@author: Naomi Chiu and Hadleigh Nunes
"""
import pygame
from pygame.locals import*
import time

class PyGameWindowView(object):
    """View object containing the visual elements of the game.
    Takes a game model and renders its state onscreen"""
    def __init__(self,model,width,height):
        self.model = model
        size = (width,height)
        self.model.screen = pygame.display.set_mode(size)

    def _init_draw(self):
        """Draws the grid on the screen and is only called at the beginning of a game."""
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
        """Draws the player paths and is updated and redrawn constantly"""
        self.model._draw_players()
        pygame.display.update()

class TronModelView(object):
    """Model object containing the players, the game state, all cells, and the cells that have been hit."""
    def __init__(self,cell_length,width,height):
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
        for i in range(self.height//cell_length):
            for j in range(self.width//cell_length):
                self.cell_lst.append(Cell((i*self.cell_length,j*self.cell_length),cell_length))
        self.game_over = False

    def _draw_players(self):
        """Calls the player objects' draw functions"""
        self.player1.draw()
        self.player2.draw()

    def in_cell(self):
        """Loops through cell_lst to find the cell whose xrange contains player.x
        and whose yrange contains player.y, and sets the player location to be within that cell."""
        for cell in self.cell_lst:
            if self.player1.x in cell.xrange and self.player1.y in cell.yrange:
                self.player1.current_cell = cell
                break
        for cell in self.cell_lst:
            if self.player2.x in cell.xrange and self.player2.y in cell.yrange:
                self.player2.current_cell = cell
                break

    def update(self):
        """Checks for new inputs and updates the game model."""
        self.player1.update()
        self.player2.update()
        if self.player1.crash():
            self.end_game("GREEN ")
        if self.player2.crash():
            self.end_game("ORANGE ")

        last_seen_p1 = self.player1.current_cell
        last_seen_p2 = self.player2.current_cell
        # Saving the player locations before updating in order to test to see if the players
        #have entered a new cell.
        self.in_cell()
        if self.player1.current_cell != last_seen_p1:
            self.player_paths.append(last_seen_p1)
        if self.player2.current_cell != last_seen_p2:
            self.player_paths.append(last_seen_p2)
        #If the player has left a cell and moved into another, the vacated cell is
        #added to the list of cells that have been hit

        if self.player1.current_cell in self.player_paths:
            self.end_game("GREEN ")
        if self.player2.current_cell in self.player_paths:
            self.end_game("ORANGE ")

    def end_game(self,player):
        """Contains end game protocol"""
        pygame.display.set_caption(player + "WINS!")
        self.game_over = True
        self.player1.dir = "None"
        self.player2.dir = "None"

class Cell(object):
    """Square object with area and location
    Used as building block for game grid"""
    def __init__(self, coords, cell_length):
        self.xrange = range(coords[0],coords[0]+cell_length)
        self.yrange = range(coords[1],coords[1]+cell_length)

class Cellview(object):
    """Cell object defining the visualized form of a cell.
    Not used structurally to define player locations, but used to visualize the game"""
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
    """Contains player's location, direction and speed, as well as their color"""
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
        """Checks if players have changed directions, and then
        adds the correct number of pixels to the player's position in the relevant direction"""
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
        """Determines what happens if a player runs of the screen.
        Used by the model to check if a player has lost."""
        if self.x == 640 or self.x == -10:
            return True
        if self.y == -10 or self.y == 480:
            return True
        return False


class KeyControl(object):
    """Assigns key strokes as actions and implements them in game model"""
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        if event.type != KEYDOWN:
            return #if no keys were pressed it quits
        if event.key == pygame.K_LEFT and self.model.game_over != True:
            if self.model.player1.dir != "r":
                self.model.player1.dir = "l"
        if event.key == pygame.K_RIGHT and self.model.game_over != True:
            if self.model.player1.dir != "l":
                self.model.player1.dir = "r"
        if event.key == pygame.K_DOWN and self.model.game_over != True:
            if self.model.player1.dir != "u":
                self.model.player1.dir = "d"
        if event.key == pygame.K_UP and self.model.game_over != True:
            if self.model.player1.dir != "d":
                self.model.player1.dir = "u"

        if event.key ==pygame.K_a and self.model.game_over != True:
            if self.model.player2.dir != "r":
                self.model.player2.dir = "l"
        if event.key == pygame.K_d and self.model.game_over != True:
            if self.model.player2.dir != "l":
                self.model.player2.dir = "r"
        if event.key == pygame.K_s and self.model.game_over != True:
            if self.model.player2.dir != "u":
                self.model.player2.dir = "d"
        if event.key == pygame.K_w and self.model.game_over != True:
            if self.model.player2.dir != "d":
                self.model.player2.dir = "u"

        if event.key == pygame.K_SPACE and self.model.game_over == True:
            return True

if __name__ == '__main__':

    def main_loop():
        """A nested loop which initializes the game and runs the model until the end game protocol is called.
        Hitting the space bar after a game ends reinitializes the loop which allows for a new match"""
        pygame.init()
        running = True
        while running:
            model = TronModelView(10,640,480)
            view = PyGameWindowView(model,640,480)
            view._init_draw()
            controller = KeyControl(model)

            game_over = False
            while not game_over:
                for event in pygame.event.get():
                    if event.type == QUIT: #if the window is closed, break out of the two while loops and go to pygame.quit()
                        running = False
                        game_over = True
                    if controller.handle_event(event): #checks to see if the game has ended and the spacebar was pressed, if yes then the inner loop is broken and the game is reinitialized
                        game_over = True
                    controller.handle_event(event) #handles regular keypress events
                model.update()
                view.draw()
                time.sleep(.1)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
        pygame.quit()

    main_loop()
