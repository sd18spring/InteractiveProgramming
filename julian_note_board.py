import pygame
from pygame.locals import *
import time

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
                             self.note_colors[self.notes[i]])
            self.note_blocks.append(note)

    def __str__(self):
        output_lines = []

        for note in self.note_blocks:
            output_lines.append(str(note))

        return "\n".join(output_lines)

class NoteBlock(object):

    def __init__(self, note, height, width, x, y, color):
        self.note = note
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        note_block_string = 'Note Block: "' + self.note + '", '
        note_block_string += 'height=%f, width=%f, x=%f, y=%f' % (self.height,
                                                                  self.width,
                                                                  self.x,
                                                                  self.y)
        return note_block_string

if __name__ == '__main__':
    pygame.init()

    size = (1860,1020)

    model = NoteBoardModel(size)
    print(model)
    view = PyGameWindowView(model, size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        view.draw()
        time.sleep(.001)

    pygame.quit()
