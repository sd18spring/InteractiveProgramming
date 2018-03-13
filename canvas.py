import numpy as np
import cv2
import random


class canvas():

    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.new_canvas = np.zeros((self.height, self.width, 3), np.uint8)
        self.randx = []
        self.randy = []
        #white,red, green, blue, yellow, purple, orange
        self.colorlist = [(255,255,255), (0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,188), (0,15,255)]

    def set_color(self, B, G, R):
        self.color = (B, G, R)

    def set_bgColor(self):
        self.new_canvas[:, :] = self.color

    def show_canvas(self):
        cv2.imshow('newCanvas', self.new_canvas)

    def save_drawing(self):
        """This function allows users to save their drawing with a name of
        their choice.
        """
        file_name = input('Please name your drawing: ')
        cv2.imwrite(file_name+'.jpg', self.new_canvas)

    def clear(self):
        """This function clears the screen.
        """
        canvas.new_canvas = np.zeros((canvas.height, canvas.width, 3), np.uint8)

    def rectangle(self):
        xpos = random.choice(self.randx)
        ypos = rand.choice(self.randy)
        color = rand.choice(self.colorlist)
        cv2.rectangle(self.new_canvas, (xpos, ypos), (10,10), color)

if __name__ == "__main__":
    canvas1 = canvas(1280, 960)
    canvas1.set_color(0, 0, 0)
    canvas1.set_bgColor()
    # cam = cv2.VideoCapture(0)
    # print(cam.get(3), cam.get(4))
    while True:
        canvas1.show_canvas()
        if cv2.waitKey(1) & 0xFF == ord('s'):
            canvas1.save_drawing()
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
