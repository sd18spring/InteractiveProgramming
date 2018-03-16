import pygame
from pygame.locals import *
import numpy
import random
import sys
import time
import copy

MOVEDOWNFREQ = 0.1
MOVESIDEWAYSFREQ = 0.15


WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

#2048 Colors:
NUM2 = (255,177,120)
NUM4 = (237, 224, 200)
NUM8 = (242, 177, 121)
NUM16 = (245,149,99)
NUM32 = (255, 83, 13)
NUM64 = (255,10,10)
NUM128 = (237,207,114)
NUM2048 = (237,194,46)

Colors = [NUM2,NUM4,NUM8,NUM16,NUM32,NUM64,NUM128,NUM2048]

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

FPS = 25
WindowWidth = 450 #used to be 415
WindowHeight = 900 #used to be 815
BoxSize = 30
BoardWidth = 20
BoardHeight = 40
BorderColor = (255,255,255)
BGColor = (0, 0, 0)
TemplateWidth = 15
TemplateHeight = 15

XMargin = int((WindowWidth - BoardWidth * BoxSize)/2)
TopMargin = WindowHeight - (BoardHeight * BoxSize) -5

#Templates of pieces:

S_Shape = [[[180,0], [225,0], [135,45], [180,45]], [[180,0],[180,45],[225,45],[225,90]]]

Z_Shape = [[[135,0],[180,0],[180,45],[225,45]],[[225,0],[225,45],[180,45],[180,90]]]

I_Shape = [[[180,0],[180,45],[180,90],[180,135]],[[135,0],[180,0],[225,0],[270,0]]]

O_Shape = [[[180,45],[225,45],[180,90],[225,90]]]

J_Shape = [[[180,45],[180,90],[225,90],[270,90]], [[180,0],[225,0],[180,45],[180,90]],[[180,45],[225,45],[270,45],[270,90]], [[225,0],[225,45],[225,90],[180,90]]]

L_Shape = [[[180,45],[225,45],[270,45],[270,0]],[[180,0],[180,45],[180,90],[225,90]],[[180,45],[225,45],[270,45],[180,90]], [[180,0],[225,0],[225,45],[225,90]]]

T_Shape = [[[180,0],[135,45],[180,45],[225,45]],[[180,0],[180,45],[180,90],[225,45]], [[180,45],[225,45],[270,45],[225,90]],[[225,0],[225,45],[225,90],[180,45]]]



Pieces = {'S': S_Shape,
          'Z': Z_Shape,
          'J': J_Shape,
          'L': L_Shape,
          'I': I_Shape,
          'O': O_Shape,
          'T': T_Shape}


class Block():
    def __init__(self,width,height,x1,y1,val):
        self.width = width
        self.height = height
        self.x1 = x1
        self.y1 = y1
        self.val = val
        self.color = random.choice(Colors)

    def convertToPixelCoords(self):
        return (XMargin + (self.x1 * BoxSize),(TopMargin +(self.y1 * BoxSize)))

    def drawBlock(self, pixelx = None, pixely = None):
        if self.val == 0:
            return
        if pixelx == None and pixely == None:
            pixelx,pixely = convertToPixelCoords(self.x1, self.y1)
        pygame.draw.rect(DisplaySurf, (0,0,0), (pixelx + 1, pixely + 1, BoxSize - 1, BoxSize - 1))
        pygame.draw.rect(DisplaySurf, self.color, (pixelx + 1, pixely + 1, BoxSize - 4, BoxSize - 4))

    def __str__(self):
        return 'Coords are: (%.d, %.d) with val %.d' %(self.x1,self.y1,self.val)

class Piece():
    def __init__(self):
        self.shape = random.choice(list(Pieces.keys()))
        self.rotation = 0

        self.coordinates = []

        b1 = Block(20,20,Pieces[self.shape][self.rotation][0][0],Pieces[self.shape][self.rotation][0][1],1)
        b2 = Block(20,20,Pieces[self.shape][self.rotation][1][0],Pieces[self.shape][self.rotation][1][1],1)
        b3 = Block(20,20,Pieces[self.shape][self.rotation][2][0],Pieces[self.shape][self.rotation][2][1],1)
        b4 = Block(20,20,Pieces[self.shape][self.rotation][3][0],Pieces[self.shape][self.rotation][3][1],1)

        self.blocks = [b1,b2,b3,b4]


    def convertToShapeCoords(self):

        for i in self.shape[self.rotation]:
            self.coordinates = self.coordinates.append(Coordinates[Shapes[self.rotation][i]])


    def rotatePiece(self):
        xdiff = self.blocks[0].x1 - Pieces[self.shape][self.rotation][0][0]
        ydiff = self.blocks[0].y1 - Pieces[self.shape][self.rotation][0][1]


        if self.rotation < len(Pieces[self.shape]) - 1:
            self.rotation += 1

        else:
            self.rotation = 0

        self.blocks[0] = Block(20,20,Pieces[self.shape][self.rotation][0][0]+xdiff ,Pieces[self.shape][self.rotation][0][1]+ydiff,1)
        self.blocks[1] = Block(20,20,Pieces[self.shape][self.rotation][1][0]+xdiff ,Pieces[self.shape][self.rotation][1][1]+ydiff,1)
        self.blocks[2] = Block(20,20,Pieces[self.shape][self.rotation][2][0]+xdiff ,Pieces[self.shape][self.rotation][2][1]+ydiff,1)
        self.blocks[3] = Block(20,20,Pieces[self.shape][self.rotation][3][0]+xdiff ,Pieces[self.shape][self.rotation][3][1]+ydiff,1)

    def down(self):
        for block in self.blocks:
            block.y1 += 45

    def left(self):
        for block in self.blocks:
            block.x1 -= 45

    def right(self):
        for block in self.blocks:
            block.x1 += 45

    def reachedBottom(self):
        for block in self.blocks:
            if block.y1 >= 850:
                return True
        return False

class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for i in range(450):
            self.grid.append([0] * 900)

    def draw_grid(self):
        #Draws the grid
        pygame.draw.rect(DisplaySurf, BorderColor, (XMargin - 3, TopMargin - 7, (BoardWidth * BoxSize) + 8, (BoardHeight * BoxSize) + 8), 5)

        #Fill Background of board
        pygame.draw.rect(DisplaySurf, BGColor, (XMargin, TopMargin, BoxSize * BoardWidth, BoxSize * BoardHeight))

        #Draw already placed pieces
        for x in range (450):
            for y in range(900):
                if self.grid[x][y] != 0:
                    pygame.draw.rect(DisplaySurf, self.grid[x][y], (x + 1, y + 1, 45 - 4, 45 - 4))

    def addToBoard(self, piece):
        for block in piece.blocks:
            for x in range(450):
                for y in range(900):
                    if x == block.x1 and y == block.y1:
                        self.grid[x][y] = block.color

    def addShape(self,piece):
        for block in piece.blocks:
            for x in range(TemplateWidth):
                for y in range(TemplateHeight):
                    if block.val == 1:
                        block.drawBlock(x + block.x1, y + block.y1)

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WindowWidth / 2), int(WindowHeight / 2))
    DisplaySurf.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WindowWidth / 2) - 3, int(WindowHeight / 2) - 3)
    DisplaySurf.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WindowWidth / 2), int(WindowHeight / 2) + 100)
    DisplaySurf.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()

def isValidPosition(board, piece, adjx = 0, adjy = 0):
    # Return True if the piece is within the board and not colliding
    for block in piece.blocks:
        if block.x1 + (adjx*45) >= 405:
            return False
        if block.x1 + (adjx*45) <= 0:
            return False
        if block.y1 + (adjy*45) > 855:
            return False
        if board.grid[block.x1 + (adjx * 45)][block.y1 + (adjy * 45)] != 0:
            return False
    return True

def main():
    global FPSCLOCK, DisplaySurf, BASICFONT, BIGFONT, BorderColor
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WindowWidth, WindowHeight))
    BASICFONT = pygame.font.Font('freesansbold.ttf',18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 80)
    pygame.display.set_caption('Tetris!')

    showTextScreen('Tetris')
    while True: # infinite game loop
        runGame()
        showTextScreen('Game Over')

def runGame():

    board = Grid(20,40)
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    fallFreq = .25

    fallingPiece = Piece()

    while True: # game loop
        movingDown = False # note: there is no movingUp variable
        movingLeft = False
        movingRight = False
        rotate = False

        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = Piece()


            #lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP: #Lifting the hand from the key
                if (event.key == K_p):
                    # Pausing the game (Press P)
                    DisplaySurf.fill(BGCOLOR)

                    showTextScreen('Paused') # pause until a key press

            elif event.type == KEYDOWN: #Pressing a key
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) :
                    movingLeft = True
                    movingRight = False

                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = True
                    movingLeft = False

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    rotate = True

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True

        # drawing everything on the screen
        DisplaySurf.fill(BGCOLOR)
        board.draw_grid()
        board.addShape(fallingPiece)

        if movingLeft == True and isValidPosition(board,fallingPiece,adjx=-1):
            fallingPiece.left()
        if movingRight == True and isValidPosition(board,fallingPiece,adjx=1):
            fallingPiece.right()
        if movingDown == True and isValidPosition(board,fallingPiece,adjy=1):
            fallingPiece.down()
        if rotate == True:
            temp = copy.deepcopy(fallingPiece)
            temp.rotatePiece()
            if isValidPosition(board,temp):
                fallingPiece.rotatePiece()

        if isValidPosition(board,fallingPiece,adjy=1):
            fallingPiece.down()
        else: #if piece has reached the bottom
            board.addToBoard(fallingPiece) # Makes fallingPiece a part of the board drawn every step
            fallingPiece = Piece()

        pygame.display.update()
        FPSCLOCK.tick(20)
        pygame.time.delay(250)

def terminate():
    pygame.quit()

if __name__ == '__main__':
    main()
