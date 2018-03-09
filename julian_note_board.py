import pygame
from pygame.locals import *
import time
import os
from psonic import *

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

SAMPLE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch

class PyGameWindowView(object):

    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for note in self.model.note_blocks:
            pygame.draw.rect(self.screen,
                             note.color,
                             pygame.Rect(note.x,
                                         note.y,
                                         note.width,
                                         note.height))
            pygame.draw.rect(self.screen,
                             (0,0,0),
                             pygame.Rect(note.x,
                                         note.y,
                                         note.width,
                                         note.height),
                             1)
            text_font = pygame.font.Font("freesansbold.ttf",30)
            text = text_font.render(note.note,True,(0,0,0))
            self.screen.blit(text,
                             (note.x+(note.width-text.get_width())//2,
                             (note.height-text.get_height())//2))
        pygame.display.update()

class NoteBoardModel(object):

    def __init__(self,size):
        self.notes = ["Ab","A","Bb","B","C","Db","D","Eb","E","F","Gb","G"]
        self.note_colors = {"Ab" : pygame.Color(255,0,0),
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
        self.note_values = {"Ab" : 56,
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
        self.note_blocks = []

        self.width = size[0]
        self.height = size[1]
        self.note_block_width = self.width/len(self.notes)

        for i in range(len(self.notes)):
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

    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x = event.pos[0]
            note_index = int(x//(size[0]/12))
            note = model.note_blocks[note_index]
            print(note)
            play_note(note.value)
            return


def play_note(val, beats=1, bpm=10000, amp=1):
    """Play note for `beats` beats. Return when done."""
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
    print(model)
    view = PyGameWindowView(model, size)
    #controller = PyGameMouseController(model)
    controller = PyGameKeyboardController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
        time.sleep(.001)

    pygame.quit()
