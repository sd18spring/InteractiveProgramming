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

def find_center():
    ret,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape,np.uint8)

    max_area=0

    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
    cnt=contours[ci]
    hull = cv2.convexHull(cnt)
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00

    centr=(cx,cy)
    cv2.circle(img,centr,5,[0,0,255],2)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
    cv2.drawContours(drawing,[hull],0,(0,0,255),2)

    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)

    if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               shape = 0
               if type(defects) != 'NoneType':
                  shape = defects.shape[0]
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    dist = cv2.pointPolygonTest(cnt,centr,True)
                    cv2.line(img,start,end,[0,255,0],2)

                    cv2.circle(img,far,5,[0,0,255],-1)
               print(i)
               i=0
    cv2.imshow('output',drawing)
    cv2.imshow('input',img)
    return cx

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

    cap = cv2.VideoCapture(0)
    while( cap.isOpened() ) :
        ret,img = cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        _, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros(img.shape,np.uint8)

        max_area=0

        for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
        cnt=contours[ci]
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00

        centr=(cx,cy)
        cv2.circle(img,centr,5,[0,0,255],2)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
        cv2.drawContours(drawing,[hull],0,(0,0,255),2)

        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)

        if(1):
                   defects = cv2.convexityDefects(cnt,hull)
                   mind=0
                   maxd=0
                   shape = 0
                   if type(defects) != 'NoneType':
                      shape = defects.shape[0]
                   for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])
                        dist = cv2.pointPolygonTest(cnt,centr,True)
                        cv2.line(img,start,end,[0,255,0],2)

                        cv2.circle(img,far,5,[0,0,255],-1)
                   print(i)
                   i=0
        cv2.imshow('output',drawing)
        cv2.imshow('input',img)

        k = cv2.waitKey(10)
        if k == 27:
            break

    pygame.quit()
