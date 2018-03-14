import pygame
from math import cos,sin,sqrt,radians,atan

pygame.init()

class GUI():
    WHITE = (255,255,255)
    font = pygame.font.SysFont("couriernew",32)
    bx = 150
    by = 100

    def __init__(self,gD):
        self.gD = gD

    def update(self,score):
        box = pygame.surface.Surface((self.bx, self.by))
        # txt_surf = self.font.render("score", True, self.WHITE)  # headline
        # txt_rect = txt_surf.get_rect(center=(self.bx//2, 30))
        # box.blit(txt_surf, txt_rect)
        txt_surf = self.font.render(str(score), True, self.WHITE)  # bottom line
        txt_rect = txt_surf.get_rect(center=(self.bx//2, 40))
        box.blit(txt_surf, txt_rect)
        self.gD.blit(box,(0,0))


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    #DOES NOT WORK

    loc = image.get_rect().center  #rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    # rot_sprite.get_rect().center = loc
    rotRect = rot_sprite.get_rect()
    rotRect.center = loc
    return rot_sprite,rotRect

class Ship():
    """Ship class!
    Holds data on ship:
    angle (degress)
    x_speed
    y_speed
    x (position)
    y (position)
    oImage (img) original
    nImage (img) new
    drift (boolean)
    rect (pygame surface)

    """
    x_speed = 0
    y_speed = 0
    drift = False
    def __init__(self,x,y,angle,img,gD):
        """
        Initliazes with where the ship is facing as the angle
        """
        self.angle = angle
        self.x = x
        self.y = y
        self.oImage = img
        self.nImage = img
        self.w,self.h = img.get_size()
        self.gD = gD
        self.rect = img.get_rect()
    def move(self):
        """FORWARD!!!
        Moves the ship forward in the direction it's heading (its angle)
        """
        self.drift = False
        self.x_speed += cos(radians(self.angle))*.4
        self.y_speed += sin(radians(self.angle))*.4
        # if sqrt(self.x_speed**2+self.y_speed**2) < 10:

    def rotate(self,posNeg):
        """Rotates ship"""
        self.nImage,self.rect = rot_center(self.oImage,posNeg*3+(270-self.angle))
        self.angle -= posNeg*3

    def update(self):
        """MAGIC
        Does magic and makes the ship work.
        Updates position
        """
        width,height = self.gD.get_size()
        speed = sqrt(self.x_speed**2+self.y_speed**2)
        # print(speed)
        if speed < .08 and self.drift:
            self.drift = False
            self.x_speed = 0
            self.y_speed = 0
        if speed > 10:
            self.x_speed = cos(radians(self.angle))*10
            self.y_speed = sin(radians(self.angle))*10
        if self.drift:
            #theta = atan(self.y_speed/self.x_speed)
            self.x_speed *= .98
            self.y_speed *= .98

        self.y += self.y_speed
        self.x += self.x_speed

        if(self.x >= width):
            self.x = 0 - self.w
        elif(self.x <= 0 - self.w):
            self.x = width
        if(self.y >= height):
            self.y = 0 - self.h
        elif(self.y <= 0 - self.h):
            self.y = height

        self.rect.center = (self.x,self.y)

        self.gD.blit(self.nImage,self.rect)
