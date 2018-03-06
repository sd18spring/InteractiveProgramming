import json
import pygame, sys
from pygame.locals import *
import math

'''Takes the latitude and longitudes of the state borders and stores them in point objects.'''

class Point(object):
    '''Represents a point in 2-D space

    '''

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

with open('states.json', 'r') as f:
    datastore = json.load(f)

def get_x(width, lng):
    return int(round(math.fmod((width * (180.0 + lng) / 360.0), (1.5 * width))))

def get_y(width, height, lat):
    lat_rad = lat * math.pi / 180.0
    merc = 0.5 * math.log( (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)) )
    return int(round((height / 2) - (width * merc / (2 * math.pi))))

state_borders = {}
all_points_list = []
for state in datastore:
    points_list = []
    for coord in datastore[state]["Coordinates"]:
        #pt = Point()
        #pt.x = coord["lat"]
        #pt.y = coord["lng"]
        #points_list.append((get_x(coord['lng']*7+200), get_y(coord['lat']*7+1300)))
        points_list.append((get_x(3000, coord['lng']), get_y(3000, 2000, coord['lat'])))
        #point_list.append(pt)
        #all_points_list.append((abs(coord['lat'])*3, abs(coord['lng'])*3))
        #all_points_list.append((coord['lat']*7+200, coord['lng']*7+1300))
    state_borders[state] = points_list
#print(state_borders)
print(all_points_list)

pygame.init()
screen = pygame.display.set_mode((1500, 1500))
white = (255,255,255)
black = (0, 0, 0)

while (True):

   # check for quit events
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();

   # erase the screen
   screen.fill(white)

   # draw the updated picture

   #updatePoints(points)  # changes the location of the points
   for state in state_borders:
       pygame.draw.polygon(screen,black,state_borders[state],1)  # redraw the points

   # update the screen
   pygame.display.update()
