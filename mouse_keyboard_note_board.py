import pygame
from pygame.locals import *
import time
import os
from psonic import *

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

SAMPLE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch

class PyGameWindowView(object):
    """
    This class draws the graphics of the program, which only consists of a
    static image of 12 rectangles, each with a note on them.
    """
    def __init__(self, model, size):
        self.model = model # Use note board model as the model
        self.screen = pygame.display.set_mode(size) # Set size of screen

    def draw(self):
        """Draws the entire note board"""
        self.screen.fill(pygame.Color(0,0,0)) # Set background color to black
        for note in self.model.note_blocks:
            pygame.draw.rect(self.screen, # Draw note block
                             note.color,
                             pygame.Rect(note.x,
                                         note.y,
                                         note.width,
                                         note.height))
            pygame.draw.rect(self.screen, # Draw a black border around note block
                             (0,0,0),
                             pygame.Rect(note.x,
                                         note.y,
                                         note.width,
                                         note.height),
                             1)
            text_font = pygame.font.Font("freesansbold.ttf",30) # Make a font
            text = text_font.render(note.note,True,(0,0,0)) # Make the note's name into a text box
            self.screen.blit(text, # Create text box at center of note block
                             (note.x+(note.width-text.get_width())//2,
                             (note.height-text.get_height())//2))
        pygame.display.update()

class NoteBoardModel(object):
    """
    This class houses the collection of notes on the noteboard. It initiallizes
    What notes are contained, their Sonic Pi note values, the colors they
    have on the graphical noteboard, and the positions they have on the noteboard.
    """
    def __init__(self,size):
        self.notes = ["Ab","A","Bb","B","C","Db","D","Eb","E","F","Gb","G"] #Note names
        self.note_colors = {"Ab" : pygame.Color(255,0,0), #Colors for the graphics
                            "A" : pygame.Color(255,128,0),
                            "Bb" : pygame.Color(255,255,0),
                            "B" : pygame.Color(128,255,0),
                            "C" : pygame.Color(0,255,0),
                            "Db" : pygame.Color(0,255,128),
                            "D" : pygame.Color(0,255,255),
                            "Eb" : pygame.Color(0,128,255),
                            "E" : pygame.Color(0,0,255),
                            "F" : pygame.Color(128,0,255),
                            "Gb" : pygame.Color(255,0,255),
                            "G" : pygame.Color(255,0,128)}
        self.note_values = {"Ab" : 56, #Sonic Pi note values
                            "A" : 57,
                            "Bb" : 58,
                            "B" : 59,
                            "C" : 60,
                            "Db" : 61,
                            "D" : 62,
                            "Eb" : 63,
                            "E" : 64,
                            "F" : 65,
                            "Gb" : 66,
                            "G" : 67}
        self.note_blocks = [] # List containing NoteBlock objects
        self.width = size[0] # Width of screen
        self.height = size[1] # Height of screen
        self.note_block_width = self.width/len(self.notes) # Width of note blocks

        for i in range(len(self.notes)): # Create and insert the note blocks
            note = NoteBlock(self.notes[i],
                             self.height,
                             self.note_block_width,
                             i*self.note_block_width,
                             0,
                             self.note_colors[self.notes[i]],
                             self.note_values[self.notes[i]])
            self.note_blocks.append(note)

    def __str__(self):
        output_lines = []

        for note in self.note_blocks:
            output_lines.append(str(note))

        return "\n".join(output_lines)

class NoteBlock(object):
    """
    This class makes a Note Block which has its size, position, Sonic Pi note
    value, and its color on the graphical note board.
    """
    def __init__(self, note, height, width, x, y, color, value):
        self.note = note
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color
        self.value = value

    def __str__(self):
        note_block_string = 'Note Block: "' + self.note + '", '
        note_block_string += 'height=%f, width=%f, x=%f, y=%f' % (self.height,
                                                                  self.width,
                                                                  self.x,
                                                                  self.y)
        return note_block_string

class PyGameKeyboardController(object):
    """
    This class controls any interactions the user has with the keyboard. Specifically,
    this class plays notes based on what key is pressed. The notes are tied, in
    order, to the top row of letter keys. This starts with "Q" and ends with the
    "]" key. If any of these keys are pressed, play their respective note.
    Otherwise, ignore key presses.
    """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_q:
            play_note(self.model.note_values.get("Ab",0))
            return
        if event.key == pygame.K_w:
            play_note(self.model.note_values.get("A",0))
            return
        if event.key == pygame.K_e:
            play_note(self.model.note_values.get("Bb",0))
            return
        if event.key == pygame.K_r:
            play_note(self.model.note_values.get("B",0))
            return
        if event.key == pygame.K_t:
            play_note(self.model.note_values.get("C",0))
            return
        if event.key == pygame.K_y:
            play_note(self.model.note_values.get("Db",0))
            return
        if event.key == pygame.K_u:
            play_note(self.model.note_values.get("D",0))
            return
        if event.key == pygame.K_i:
            play_note(self.model.note_values.get("Eb",0))
            return
        if event.key == pygame.K_o:
            play_note(self.model.note_values.get("E",0))
            return
        if event.key == pygame.K_p:
            play_note(self.model.note_values.get("F",0))
            return
        if event.key == pygame.K_LEFTBRACKET:
            play_note(self.model.note_values.get("Gb",0))
            return
        if event.key == pygame.K_RIGHTBRACKET:
            play_note(self.model.note_values.get("G",0))
            return

class PyGameMouseController(object):
    """
    This class controls any interactions the user has with the mouse. This class
    will detect when there is a left click. It will get the position of the mouse
    at the time of a click, turn that position into a note index so it can detect
    which note block is being clicked, and will then play the respective note.
    """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x = event.pos[0] # Gets x position of mouse
            note_index = int(x//(size[0]/12)) # Turns position into note index
            note = model.note_blocks[note_index] # Finds the note from that index
            play_note(note.value) # Plays the note
            return
        else:
            return

def play_note(val, beats=1, bpm=600, amp=1):
    """This function references Sonic Pi to play the specified note."""
    # `note` is this many half-steps higher than the sampled note
    half_steps = val - SAMPLE_NOTE
    # An octave higher is twice the frequency. There are twelve half-steps per
    # octave. Ergo, each half step is a twelth root of 2 (in equal temperament).
    rate = (2 ** (1 / 12)) ** half_steps
    # Turn sample into an absolute path, since Sonic Pi is executing from a
    # different working directory.
    sample(os.path.realpath(SAMPLE_FILE), rate=rate, amp=amp)

if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    model = NoteBoardModel(size)
    view = PyGameWindowView(model, size)
    mouse_con = PyGameMouseController(model) # Initializes the mouse controller
    keyboard_con = PyGameKeyboardController(model) # Initializes the keyboard controller

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            mouse_con.handle_event(event) # If mouse click, act as needed
            keyboard_con.handle_event(event) # If key press, act as needed
        view.draw()
        time.sleep(.001)

    pygame.quit()
