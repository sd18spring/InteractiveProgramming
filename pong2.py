import pygame
from pygame.locals import *
import time
import numpy as np
import cv2



class PyGameWindowView(object):
    """ A view of the Pong game rendered in a PyGame Window"""
    def __init__(self, model, size):
        """ Initialize the PyGame window of the game """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """Draw the current game state to the screen"""
        self.screen.fill(pygame.Color(135, 206, 250))
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 127, 80),
                        pygame.Rect(self.model.paddle1.x,
                                    self.model.paddle1.y,
                                    self.model.paddle1.width,
                                    self.model.paddle1.height))
        pygame.draw.rect(self.screen,
                        pygame.Color(255, 127, 80),
                        pygame.Rect(self.model.paddle2.x,
                                    self.model.paddle2.y,
                                    self.model.paddle2.width,
                                    self.model.paddle2.height))

        pygame.draw.circle(self.screen,
                           pygame.Color(255,255,102),
                           (self.model.ball.x,
                           self.model.ball.y),
                           self.model.ball.radius)

        pygame.display.update()


class PongModel(object):
    """Encodes a model of the game state"""

    def __init__(self,size):
        self.width = size[0]
        self.height = size[1]
        self.paddle1 = Paddle(100, 20, 10, self.height)
        self.paddle2 = Paddle(100, 20, self.width - 30, self.height / 2)
        self.ball = Ball(int(self.width/2), int(self.height/2), int(10), 10)


    def update(self):

        self.paddle1.update()
        self.paddle2.update()

    def __str__(self):
        output_lines = []

        output_lines.append(str(self.paddle1))
        output_lines.append(str(self.paddle2))


        return "\n".join(output_lines)

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, speed):

        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.vy = 0.0
        self.vx = 0.0


    def update(self, ball, paddle1, paddle2, vx, vy):

        if self.ball.x == -1 and 10 == self.ball.x:
            return -1
        elif self.ball.x == 1 and self.paddle2.width == self.ball.x:
            return -1
        else:
            return 1


    def __str__(self):
        return "Ball x=%f, y=%f, radius=%f" % (self.x, self.y, self.radius)



class Paddle(pygame.sprite.Sprite):
    """Encodes the state of the paddle 1 in the game"""

    def __init__(self, height, width, x, y):
        """Initalize a paddle with the sepcified height, width, and position (x,y) """

        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = 0.0

    def update(self):
        """update the state of the paddle"""

        self.y += self.vy

    def update_position(self, coordinate):
        self.y = coordinate

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height, self.width, self.x, self.y)


def get_coordinates(cap, lower_threshold, upper_threshold):


    ret, frame = cap.read()

    hsv_scale = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)


    lower_threshold_array = np.array(lower_threshold)
    upper_threshold_array = np.array(upper_threshold)

    # creating the threshold
    # binary
    mask = cv2.inRange(hsv_scale, lower_threshold_array, upper_threshold_array)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)


    # blue moment tracking
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    coordinates = []

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        coordinates.append(center[1])

    return coordinates




if __name__ == '__main__':
    pygame.init()

    FPS = 200

    size = (1800, 1000)
    model = PongModel(size)

    view = PyGameWindowView(model, size)

    fps_clock = pygame.time.Clock()

    cap = cv2.VideoCapture(0)

    blue_lower = [110,50,50]
    blue_upper = [130,255,255]

    green_lower = [85,100,100]
    green_upper = [95,255,255]


    running = True
    while running:

        try:
            coordinate1 = get_coordinates(cap, blue_lower, blue_upper)[0] * 2
            coordinate2 = get_coordinates(cap, green_lower, green_upper)[0] * 2
            model.paddle1.update_position(coordinate1)
            model.paddle2.update_position(coordinate2)
        except IndexError:
            pass


        view.draw()
        time.sleep(.001)
        fps_clock.tick(FPS)

    pygame.quit()
