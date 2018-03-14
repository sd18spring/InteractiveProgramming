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
        self.pathlength = 10
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

    def shift(self, myList, myElement):
        return myList[1:] + [myElement]

    def find_center(self, mask, target, disappr=True):
        """This function takes in a cv2 mask, find the center of the
        contours in the mask, and draw a green dot at the center location
        on the target frame
        """
        im2, contours, hierarchy = cv2.findContours(mask, 1, 2)
        try:
            if self.frame_num > self.refreshDelay or self.frame_num == 0:
                cnt = contours[0]
                M = cv2.moments(cnt)
                #print(M['m10'] / M['m00'])
                self.cx = int(M['m10'] / M['m00'])
                self.cy = int(M['m01'] / M['m00'])
                self.frame_num = 0
                if len(self.path) <= 1:
                    self.path.append((self.cx, self.cy))
                elif len(self.path) >= 2:
                    # Calculate the distance between the two newest point.
                    pair = self.path[-1]
                    diffx = abs(self.cx-pair[0])
                    diffy = abs(self.cy-pair[1])
                    distance = math.sqrt(diffx**2+diffy**2)
                    if distance < 150:
                        # print('Far enough')
                        if len(self.path) < self.pathlength:
                            self.path.append((self.cx, self.cy))
                        else:
                            if disappr:
                                self.path = self.shift(self.path, (self.cx, self.cy))
                            else:
                                self.path.append((self.cx, self.cy))
                        dist2hue = self.map(distance, 0.0, 150.0, 0.0, 255.0)
                        paintColor = self.brush_color(dist2hue)
                        if len(self.colors) < self.pathlength:
                            self.colors.append((int(paintColor[0][0][0]), int(paintColor[0][0][1]), int(paintColor[0][0][2])))
                        else:
                            if disappr:
                                self.colors = self.shift(self.colors, (int(paintColor[0][0][0]), int(paintColor[0][0][1]), int(paintColor[0][0][2])))
                            else:
                                self.colors.append((int(paintColor[0][0][0]), int(paintColor[0][0][1]), int(paintColor[0][0][2])))
                        # print(self.colors)
            cv2.circle(target, (self.cx, self.cy), 2, (0, 255, 0), -1)
            self.notFound = False
        except IndexError:
            """"""
            self.notFound = True

    def draw(self, canvas):
        """This function draws the lines on the canvas of the screen.
        The default is that only the 20 newest points will be drawn on screen.
        """
        canvas.new_canvas = np.zeros((canvas.height, canvas.width, 3), np.uint8)
        for i in range(len(self.path)):
            if len(self.path) <= 1:
                break
            else:
                if i < len(self.path)-2:
                    cv2.line(canvas.new_canvas, self.path[i], self.path[i+1], self.colors[i], 3)

        if len(self.path) > 4:
            def det(p1, p2, p3, p4):
                deltaA = p1[0] - p2[0]
                deltaB = p1[1] - p2[1]
                deltaC = p3[0] - p4[0]
                deltaD = p3[1] - p4[1]
                return deltaA * deltaD - deltaB * deltaC
            div = det(self.path[-1], self.path[-2], self.path[-3], self.path[-4])
            if div != 0 and not self.notFound:
                """"""
                # print('the two line intersects!!!')
