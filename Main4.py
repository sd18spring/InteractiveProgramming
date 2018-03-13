import pygame
import time
import random
import cv2
import numpy as np

class PyGameWindowView(object):
    """ Provides a view of the Dodgy Game model in a pygame
        window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.bombflag = True
        self.bombflag2 = True
        self.font = "arial"
        self.font_size = 40
        self.score_str = "Score: "

    def draw(self):
        """ Draw the current game state to the screen """
        # Draw the background color
        self.screen.fill(pygame.Color(255, 255, 255))

        # Draw the bomb and make a short animation by changing between two picture
        self.bomb1 = pygame.transform.scale(
            pygame.image.load('bomb1.png'), (125, 125))
        self.bomb2 = pygame.transform.scale(
            pygame.image.load('bomb2.png'), (125, 125))
        if (self.bombflag):
            self.screen.blit(self.bomb1, (self.model.bomb.center_x, self.model.bomb.center_y))
            self.bombflag = False
        else:
            self.screen.blit(self.bomb2, (self.model.bomb.center_x, self.model.bomb.center_y))
            self.bombflag = True

        if (self.bombflag2):
            self.screen.blit(self.bomb1, (self.model.bomb2.center_x, self.model.bomb2.center_y))
            self.bombflag2 = False
        else:
            self.screen.blit(self.bomb2, (self.model.bomb2.center_x, self.model.bomb2.center_y))
            self.bombflag2 = True

        self.smile = pygame.transform.scale(
            pygame.image.load('smiley.png'),(70,70))
        self.screen.blit(self.smile, (self.model.smile.center_x, self.model.smile.center_y))

        # Draw the player
        self.player = pygame.transform.scale(
            pygame.image.load('Genie1.png'),(100,100))
        self.screen.blit(self.player, (self.model.player.center_x, self.model.player.center_y))

        self.myfont = pygame.font.SysFont(self.font, self.font_size, True)
        label = self.myfont.render(self.score_str + str(self.model.score), True, (0, 0, 0))
        self.screen.blit(label, (self.model.width - 200, 40))

        # The Lives left for player on the top left corner
        self.skeleton = pygame.transform.scale(
            pygame.image.load('skeleton.png'), (60, 60))
        for skeleton in self.model.skeletons:
            self.screen.blit(self.skeleton, (skeleton.left, skeleton.top))

        pygame.display.update()

    def gameover(self):
        self.end = pygame.transform.scale(
            pygame.image.load('gameover.jpg'), (400, 400))
        self.endpicturesize = self.end.get_size()
        self.screen.blit(self.end, ((self.size[0]-self.endpicturesize[0])/2, (self.size[1]-self.endpicturesize[1])/2))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        cap.release()
        cv2.destroyAllWindows()


class Model(object):
    def __init__(self,size):
        self.width = size[0]
        self.height = size[1]

        self.bomb_init_height = -200
        self.bomb_moving_sped = random.randrange(8,15)
        self.bomb_moving_sped_fast = random.randrange(15,20)
        self.bomb = Bomb(random.randrange(0,self.width), self.bomb_init_height, self.bomb_init_height, self.height,
                         self.width, self.bomb_moving_sped)
        self.bomb2 = Bomb(random.randrange(0, self.width), self.bomb_init_height, self.bomb_init_height, self.height,
                         self.width, self.bomb_moving_sped_fast)

        self.smile_init_height = -200
        self.smile_moving_sped = random.randrange(10,20)
        # print ("1")
        self.smile = Smile(random.randrange(0,self.width), self.smile_init_height, self.smile_init_height, self.height,
                           self.width, self.smile_moving_sped)

        self.player_init_position = 400
        self.player_y_position = 500
        self.player = User(self.player_init_position, self.player_y_position,self.width)

        self.score = 0
        self.lives = 3

        self.skeletons = []
        self.skeleton_width = 50
        self.skeleton_space = 10
        self.skeleton_left = 30
        self.skeleton_top = 30

        # if 460 <= self.bomb.center_y <= 540 and self.player.center_x - 50 <= self.bomb.center_x <= self.player.center_x + 100:
        #     self.lives -= 1
        #     # print ("1")
        #
        # for x in range(self.skeleton_left,
        #                self.skeleton_left * self.lives,
        #                self.skeleton_space):
        #     # print ("2")
        #     self.skeletons.append(Lives(x, self.skeleton_top))

    def update(self):
        self.bomb.update()
        self.bomb2.update()
        self.smile.update()
        self.player.update()

        if 460 <= self.bomb.center_y <= 540 and self.player.center_x - 50 <= self.bomb.center_x <= self.player.center_x + 100:
            # Decrease the number of lives and remove the touched bomb
            self.lives -= 1
            self.bomb.center_y = self.width + 100

        if 460 <= self.bomb2.center_y <= 540 and self.player.center_x - 50 <= self.bomb2.center_x <= self.player.center_x + 100:
            # Decrease the number of lives and remove the touched bomb
            self.lives -= 1
            self.bomb2.center_y = self.width + 100

        if 460 <= self.smile.center_y <= 540 and self.player.center_x - 50 <= self.smile.center_x <= self.player.center_x + 100:
            # Decrease the number of lives and remove the touched bomb
            self.score +=1
            # print (self.score)
            self.smile.center_y = self.width + 100


        self.skeletons = []
        for x in range(self.skeleton_left,
                       self.skeleton_left + (self.skeleton_width + self.skeleton_space) * self.lives,
                       self.skeleton_width + self.skeleton_space):
            self.skeletons.append(Lives(x, self.skeleton_top))


class Bomb(object):
    """ Represents a bomb in dodging game """
    def __init__(self, center_x, center_y, start_y, display_width, display_height, moving_speed):
        """ Create a bomb object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.start_y = start_y
        self.display_width = display_width
        self.display_height = display_height
        self.moving_speed = moving_speed

    def update(self):
        # update the position of bomb each time
        self.center_y += self.moving_speed
        # if the bomb achieve the bottom of the screen
        if self.center_y >self.display_height:
            self.center_y = self.start_y
            self.center_x = random.randrange(0, self.display_width)


class Smile(object):
    """ Represents a smile face in dodging game """
    def __init__(self, center_x, center_y, start_y, display_width, display_height, moving_speed):
        """ Create a bomb object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.start_y = start_y
        self.display_width = display_width
        self.display_height = display_height
        self.moving_speed = moving_speed

    def update(self):
        # update the position of bomb each time
        self.center_y += self.moving_speed
        # if the bomb achieve the bottom of the screen
        if self.center_y >self.display_height:
            self.center_y = self.start_y
            self.center_x = random.randrange(0, self.display_width)


class User(object):
    """ Represents the player in dodging game """

    def __init__(self, center_x, center_y, display_width):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.display_width = display_width
        self.center_x = self.display_width * 0.5 - 50

    def update(self):
        self.ret, frame = cap.read()
        self.faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 20))
        # self.center_x = self.display_width * 0.5 - 50
        for (x, y, w, h) in self.faces:
            cv2.circle(frame, (w / 2 + x, h / 2 + y), 10, (255, 255, 255), -1)
            self.center_x = (float)(x) / (400) * self.display_width
            # print (self.center_x)
            self.center_x = self.display_width - self.center_x
            # print (self.center_x)
            # print ("")

            # print (x)

        # Hardcoded cord for out of bounds center_x(Need change!!!!)
        if self.center_x >700:
            self.center_x =700

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()


class Lives(object):
    '''The number of lives the player has. Starts with 3 lives.'''

    def __init__(self, left, top ):
        self.left = left
        self.top = top


if __name__ == '__main__':

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    kernel = np.ones((40, 21), 'uint8')
    cap = cv2.VideoCapture(0)

    pygame.init()
    pygame.display.set_caption('Game')
    size = (800, 600)
    model = Model(size)
    view = PyGameWindowView(model, size)

    running = True
    while running:
        model.update()
        view.draw()
        if model.lives <= 0:
            view.gameover()
        time.sleep(.001)