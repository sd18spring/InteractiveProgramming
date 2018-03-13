#!/usr/bin/env python
#
# Sling
# A game about the controlled destruction of fruits.
#
# Amy Phung // Sid Garimella
# Software Design 2017-2018, Olin College

VERSION = "0.1"
ASSET_DIRECTORY = "assets"
RESOLUTION_X = 1000
RESOLUTION_Y = 800

ORANGE = (244, 167, 66)
GREEN = (70, 170, 73)
RED = (168, 11, 69)
YELLOW = (249, 242, 17)

BACK = (56, 30, 0)

G = 0.5
colors = [ORANGE,GREEN,RED,YELLOW]
nowFruits = []
sizeMN = 30
sizeMX = 60

""" Loads all modules/dependencies.
"""
import sys
import random
import math
import numpy as np
import os
import cv2
import time
import pygame

from pygame.locals import *


""" Game objects
"""

class Fruit(pygame.sprite.Sprite):
    """A periodically generated on-screen target.
    Returns: fruit object
    """

    def __init__(self, radius, color, vector):
        self.radius = radius
        self.color = color
        self.visible = 1
        self.vx = 0
        self.vy = 0
        self.x,self.y = vector
        self.drag = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy

class Hand(pygame.sprite.Sprite):
    def __init__(self, vector):
        self.x,self.y = vector


pygame.init()
display_a = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
pygame.display.set_caption("Sling")
display_a.fill(BACK)

mainWindow = pygame.Rect(15,15,RESOLUTION_X - 30, RESOLUTION_Y - 30)
origin = pygame.Rect(RESOLUTION_X/2 - 100, RESOLUTION_Y - 30, 190, 30)

def generateNewBall() :
    radius = random.randint(sizeMN, sizeMX)
    center = ( origin.centerx, origin.centery)
    newBall = Fruit(radius, colors[random.randint(1,4) - 1], center)
    #newBall.vy = -1*random.randint(4, 6)/3
    newBall.vy = -1*random.randint(10,16)
    newBall.vx = random.randint(-8, 8)
    nowFruits.append(newBall)

def genWaveBalls():
    if len(nowFruits) == 0:
        for i in range(3):
            generateNewBall()
        for fruit in nowFruits:
            fruit.move()
            fruit.vy = fruit.vy + fruit.drag
            fruit.drag = fruit.drag + G*0.05
            if fruit.y < RESOLUTION_Y:
                pygame.draw.circle(display_a, fruit.color, (int(fruit.x), int(fruit.y)), fruit.radius, 0)
    else:
        for fruit in nowFruits:
            fruit.move()
            fruit.vy = fruit.vy + fruit.drag
            fruit.drag = fruit.drag + G*0.05
            if fruit.y < RESOLUTION_Y:
                pygame.draw.circle(display_a, fruit.color, (int(fruit.x), int(fruit.y)), fruit.radius, 0)
            elif fruit.y > 15000:
                nowFruits[:] = []

def isOnFruit(vector):
    x,y = vector
    for fruit in nowFruits:
        if math.pow(x-fruit.x,2) + math.pow(y-fruit.y,2) < math.pow(fruit.radius,2):
            return fruit
    return False

""" Main loop
"""


#Open Camera object
cap = cv2.VideoCapture(0)



def nothing(x):
    pass

# Function to find angle between two vectors
def Angle(v1,v2):
 dot = np.dot(v1,v2)
 x_modulus = np.sqrt((v1*v1).sum())
 y_modulus = np.sqrt((v2*v2).sum())
 cos_angle = dot / x_modulus / y_modulus
 angle = np.degrees(np.arccos(cos_angle))
 return angle

# Function to find distance between two points in a list of lists
def FindDistance(A,B):
 return np.sqrt(np.power((A[0][0]-B[0][0]),2) + np.power((A[0][1]-B[0][1]),2))


# Creating a window for HSV track bars
cv2.namedWindow('HSV_TrackBar')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'HSV_TrackBar',0,179,nothing)
cv2.createTrackbar('s', 'HSV_TrackBar',0,255,nothing)
cv2.createTrackbar('v', 'HSV_TrackBar',0,255,nothing)


pygame.mouse.set_cursor(*pygame.cursors.diamond)

while True:

    #Measure execution time
    start_time = time.time()

    #Capture frames from the camera
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    #Blur the image
    blur = cv2.blur(frame,(3,3))

 	#Convert to HSV color space
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    #Create a binary image with where white will be skin colors and rest is black
    mask2 = cv2.inRange(hsv,np.array([2,50,50]),np.array([15,255,255])) #for skin colors
    #tolerance = 30
    #mask2 = cv2.inRange(hsv,np.array([60-tolerance,50,50]),np.array([60+tolerance,255,255]))#for green objects

    #Kernel matrices for morphological transformation
    kernel_square = np.ones((11,11),np.uint8)
    kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    #Perform morphological transformations to filter out the background noise
    #Dilation increase skin color area
    #Erosion increase skin color area
    dilation = cv2.dilate(mask2,kernel_ellipse,iterations = 1)
    erosion = cv2.erode(dilation,kernel_square,iterations = 1)
    dilation2 = cv2.dilate(erosion,kernel_ellipse,iterations = 1)
    filtered = cv2.medianBlur(dilation2,5)
    kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
    dilation2 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
    kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilation3 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
    median = cv2.medianBlur(dilation2,5)
    ret,thresh = cv2.threshold(median,127,255,0)

    #Find contours of the filtered frame
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #Draw Contours
    #cv2.drawContours(frame, cnt, -1, (122,122,0), 3)
    #cv2.imshow('Dilation',median)

	#Find Max contour area (Assume that hand is in the frame)
    max_area=100
    ci=0
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i

	#Largest area contour
    if ci>=len(contours): #Passes if color cannot be found
        pass
    else:
        cnts = contours[ci]

    #Find convex hull
    hull = cv2.convexHull(cnts)

	#Find moments of the largest contour
    moments = cv2.moments(cnts)

    #Central mass of first order moments
    if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00
    centerMass=(cx,cy)

    cx = 800*(cx-70)/(860-70)
    cy = 800*(cy-90)/(450-90)
    #Draw center mass
    cv2.circle(frame,centerMass,7,[100,0,255],2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Center',tuple(centerMass),font,2,(255,255,255),2)

    #Print x and y coordinates
    cv2.putText(frame,str(cx),(100,200),font,2,(255,255,255),2)
    cv2.putText(frame,str(cy),(100,300),font,2,(255,255,255),2)

    #Print bounding rectangle
    #x,y,w,h = cv2.boundingRect(cnts)
    #img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.drawContours(frame,[hull],-1,(255,255,255),2)

    ##### Show final image ########
    cv2.namedWindow('Dilation')
    cv2.imshow('Dilation',frame)
    cv2.moveWindow('Dilation',200,200)
    ###############################

    #Print execution time
    #print time.time()-start_time

    #close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    display_a.fill((255,255,255))
    pygame.draw.rect(display_a, BACK, mainWindow)
    genWaveBalls()




    pygame.draw.circle(display_a, (255,255,255), (int(cx)*2, int(cy)), 10, 0)

    if isOnFruit((cx*2,cy)) is not False:
        nowFruits.remove(isOnFruit((cx*2,cy)))

    #event = pygame.event.poll()

    #if event.type == pygame.MOUSEMOTION:
    #    currx, curry = event.pos

    #if event.type == pygame.MOUSEBUTTONDOWN:
    #    x1, y1 = event.pos


    #if event.type == pygame.MOUSEBUTTONUP:
    #    x2, y2 = event.pos


    pygame.display.update()

cap.release()
cv2.destroyAllWindows()
