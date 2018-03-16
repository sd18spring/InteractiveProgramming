import pygame
from pygame.locals import *
import numpy
import random
import sys
import time

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

Colors = [RED,GREEN,BLUE,YELLOW]

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

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

Coordinates = {'1': [135,0],
               '2': [180,0],
               '3': [225,0],
               '4': [270,0],
               '5': [135,45],
               '6': [180,45],
               '7': [225,45],
               '8': [270,45],
               '9': [135,90],
               '10': [180,90],
               '11': [225,90],
               '12': [270,90],
               '13': [135,135],
               '14': [180,135],
               '15': [225,135],
               '16': [270,135]}




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

    def drawPiece(self,pixelx=None,pixely=None):
        """
        if b.val == 0:
            return
        if pixelx == None and pixely == None:
            pixelx = b.x1
            pixely = b.y1

        pygame.draw.rect(DisplaySurf, (0,0,0), (pixelx + 1, pixely + 1, BoxSize - 1, BoxSize - 1))
        pygame.draw.rect(DisplaySurf, (34,89,233), (pixelx + 1, pixely + 1, BoxSize - 4, BoxSize - 4))
        """
        pass

    def rotatePiece(self):
        xdiff = self.x1 - Pieces[self.shape][self.rotation][0][0]
        ydiff = self.y1 - Pieces[self.shape][self.rotation][0][1]


        if self.rotation < len(Pieces[self.shape]) - 1:
            self.rotation += 1

        else:
            self.rotation = self.rotation[0]

        self.x1 = Pieces[self.shape][self.rotation][0][0] + xdiff
        self.y1 = Pieces[self.shape][self.rotation][0][1] + ydiff

    def translate():
        #Loop through blocks and change x y coords
        #localize block to its own coordinate system, so that it can be defined by one point
        #Need a get-block positions () function to get block x and y coords
        pass






class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
    def append(self, thing):
        self.grid.append(thing)
    def make_grid(self):
        self.grid = []
        for i in range(self.width):
            self.append([0] * self.height)
        return self.grid

    def draw_grid(self):
        #Draws the grid
        pygame.draw.rect(DisplaySurf, BorderColor, (XMargin - 3, TopMargin - 7, (BoardWidth * BoxSize) + 8, (BoardHeight * BoxSize) + 8), 5)

        #Fill Background of board
        pygame.draw.rect(DisplaySurf, BGColor, (XMargin, TopMargin, BoxSize * BoardWidth, BoxSize * BoardHeight))

        #Draw individual boxes
       #or x in range (BoardWidth):
            #or y in range(BoardHeight):
                #elf.block.drawBlock(x,y)

    """def addToBoard(self, piece):
        for block in piece.blocks:
            for x in range(TemplateWidth):
                for y in range(TemplateHeight):
                    if block.val == 1:
                        self.grid[block.x1][block.y1] = block.color"""

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
        FPSCLOCK.tick()

def isOnBoard(x,y):
    return x >= 0 and x < BoardWidth and y < BoardHeight


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for block in piece.blocks:
        for x in range(TemplateWidth):
            for y in range(TemplateHeight):
                isAboveBoard =  y + block.y1 + adjY < 0
                if isAboveBoard or block.val == 0:
                    continue
                if not isOnBoard(x + block.x1 + adjX, y + block.y1 + adjY):
                    return False
                if board[x + block.x1 + adjX][y + block.y1 + adjY] != 0:
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
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    fallFreq = .25

    fallingPiece = Piece()
    nextPiece = Piece()



    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = Piece()
            print(nextPiece)

            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game (Press P)
                    DisplaySurf.fill(BGCOLOR)

                    showTextScreen('Paused') # pause until a key press

                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                    #move left press a
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                    #move right press d
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                    #move down press s
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece.x1 -= 25
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece.x1 += 25
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    if isValidPosition(board, fallingPiece):
                        fallingPiece.rotatePiece()



                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece.y1 += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece.y1 += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece.x1 -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece.x1 += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece.y1 += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                board.addShape(fallingPiece)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece.y1 += 45
                lastFallTime = time.time()

        # drawing everything on the screen
        DisplaySurf.fill(BGCOLOR)
        board.make_grid()
        board.draw_grid()

        if fallingPiece == None:
            nextPiece = Piece()
            board.addShape(nextPiece)



        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()

if __name__ == '__main__':
    main()
