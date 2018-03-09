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

    def BGR2HSV(self, frame):
        """This functions takes in a frame and converts it from BGR to BGR2HSV
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def red_mask(self, frame):
        """This function generates a red mask based on the frame being passed in
        """
        mask1 = cv2.inRange(frame, self.red_maskL[0], self.red_maskH[0])
        mask2 = cv2.inRange(frame, self.red_maskL[1], self.red_maskH[1])
        return (mask1 | mask2)

    def find_center(self, mask, target):
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

    def draw(self, target):
        if len(self.path) == 1:
            clearpath.append(path[0])
        elif len(self.path) > 2:
            pair = self.path[-2]
            # print(pair, pair[0], cx, pair[1], cy)
            diffx = abs(self.cx-pair[0])
            diffy = abs(self.cy-pair[1])
            distance = math.sqrt(diffx**2+diffy**2)
            if distance<10:
                self.clearpath.append(pair)
        for i in range(len(self.path)):
            # TODO: Add if statements to make sure that any outliers
            # would be removed from the list or ignored when drawing
            # the linewidth
            diffx = math.abs(self.cx-self.path[-1][0])
            print(diffx)
            diffy = math.abs(cy-path[-1][1])
            print(diffy)
            if len(self.path) == 1:
                break
            # elif math.sqrt(diffx**2+diffy**2) > 30:
                # break
            if i < (len(self.clearpath)-1):
                cv2.line(target, self.clearpath[i], self.path[i+1], (255, 0, 0), 3)
