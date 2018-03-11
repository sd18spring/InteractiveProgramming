import numpy as np
import cv2
import math


class finger_track():

    def __init__(self):
        """
        """
        self.frame_num = 0
        self.cx = 0
        self.cy = 0
        self.path = []
        self.clearpath = []
        self.red_maskL = [np.array([0, 150, 100]), np.array([178, 150, 100])]
        self.red_maskH = [np.array([1, 255, 255]), np.array([180, 255, 255])]
        self.refreshDelay = 0
        self.colors = []
        self.dist = []

    def map(self, x, oldL, oldH, newL, newH):
        """This function maps a value from one range to a differnet range

        x: the value in the old range
        oldL: the lower limit of the old range of values
        oldH: the upper limit of the old range of values
        newL: the lower limit of the new range of values
        newH: the upper limit of the new range of values
        """
        return int(((x - oldL)/(oldH-oldL))*(newH-newL)+newL)

    def brush_color(self, hue):
        """This function takes in a uint8 value for hue and generate
        a BGR color range """
        color = np.uint8([[[hue, 255, 255]]])
        return cv2.cvtColor(color, cv2.COLOR_HSV2BGR)

    def BGR2HSV(self, frame):
        """This functions takes in a frame and converts it from BGR
        to HSV values
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def red_mask(self, frame):
        """This function generates a red mask based on the frame being
        passed in
        """
        mask1 = cv2.inRange(frame, self.red_maskL[0], self.red_maskH[0])
        mask2 = cv2.inRange(frame, self.red_maskL[1], self.red_maskH[1])
        return (mask1 | mask2)

    def find_center(self, mask, target):
        """This function takes in a cv2 mask, find the center of the
        contours in the mask, and draw a green dot at the center location
        on the target frame
        """
        im2, contours, hierarchy = cv2.findContours(mask, 1, 2)
        try:
            if self.frame_num > self.refreshDelay or self.frame_num == 0:
                cnt = contours[0]
                M = cv2.moments(cnt)
                print(M['m10'] / M['m00'])
                self.cx = int(M['m10'] / M['m00'])
                self.cy = int(M['m01'] / M['m00'])
                self.frame_num = 0
                self.path.append((self.cx, self.cy))
            cv2.circle(target, (self.cx, self.cy), 2, (0, 255, 0), -1)
        except IndexError:
            """"""

    def refine_path(self):
        """This function takes evalutes every two consecutive points,
        find the distance between them, and add the new point to a
        list of clear path if they are not off by roughly 15 pixels.
        It also takes a distance and convert it to a color to be used
        when plotting the line.
        """
        if len(self.path) == 1:
            self.clearpath.append(self.path[0])
        elif len(self.path) > 2:
            pair = self.path[-2]
            diffx = abs(self.cx-pair[0])
            diffy = abs(self.cy-pair[1])
            distance = math.sqrt(diffx**2+diffy**2)
            if distance<10:
                dist2hue = self.map(distance, 0.0, 10.0, 0.0, 255.0)
                paintColor = self.brush_color(dist2hue)
                self.colors.append((int(paintColor[0][0][0]), int(paintColor[0][0][1]), int(paintColor[0][0][2])))
                self.clearpath.append(pair)

    def draw(self, canvas, disappr=True):
        """This function draws the lines on the canvas of the screen.
        The default is that only the 20 newest points will be drawn on screen.
        """
        for i in range(len(self.clearpath)):
            if len(self.clearpath) < 1:
                break
            elif i<(len(self.clearpath)-1)<21:
                cv2.line(canvas.new_canvas, self.clearpath[i], self.clearpath[i+1], self.colors[i], 3)
            elif 20 < i < (len(self.clearpath)-1):
                canvas.new_canvas = np.zeros((canvas.height, canvas.width, 3), np.uint8)
                for j in range(20):
                    cv2.line(canvas.new_canvas, self.clearpath[-(j+1)], self.clearpath[-(j+2)], self.colors[-(j+2)], 3)
