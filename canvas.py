import numpy as np
import cv2


class canvas():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.new_canvas = np.zeros((self.height, self.width, 3), np.uint8)

    def set_color(self, B, G, R):
        self.color = (B, G, R)

    def set_bgColor(self, B, G, R):
        self.new_canvas[:, :] = self.color

    def show_canvas(self):
        cv2.imshow(self.new_canvas)
