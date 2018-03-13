import json
import pygame, sys
from pygame.locals import *
import math
import random
import csv

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
        points_list.append((get_x(4000, coord['lng']), get_y(4000, 2300, coord['lat'])))
        #point_list.append(pt)
        #all_points_list.append((abs(coord['lat'])*3, abs(coord['lng'])*3))
        #all_points_list.append((coord['lat']*7+200, coord['lng']*7+1300))
    state_borders[state] = points_list
#print(state_borders)
# for state in state_borders:
    # print(state_borders[state])

numbers = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '-': 0}

hospitals = {}
with open('Hospitals.csv', newline='') as csvfile:
    hospitaldata = csv.reader(csvfile)#, delimiter=' ')
    for hospital in hospitaldata:
        if len(hospital) > 4 and hospital[0][0] in numbers:
            lng = hospital[0]
            lat = hospital[1]
            name = hospital[4]
            hospitals[str(name)] = (get_x(4000, float(lng)), get_y(4000, 2300, float(lat)))

#credit for following function to: http://www.ariel.com.au/a/python-point-int-poly.html
def is_in_polygon(x, y, points):
    n = len(points)
    inside = False
    px1, py1 = points[0]
    for i in range(1, n + 1):
        px2, py2 = points[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y-py1)*(px2-px1)/(py2-py1)+px1
                    if px1 == px2 or x <= xinters:
                        inside = not inside
        px1, py1 = px2, py2
    return inside

pygame.init()
size = (1500, 1500)
screen = pygame.display.set_mode(size)
background = pygame.image.load('USflag.png')
background = pygame.transform.scale(background, size)

#pygame.display.flip()
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

colors = {(255,0,0): 'red', (0,255,0): 'green', (0,0,255): 'blue', (0,0,128): 'darkBlue', (255,255,255): 'white', (0,0,0): 'black', (255,200,200): 'pink'}

# state_colors = []
# for i in range(50):
#     state_colors.append(random.choice(list(colors)))
#
# i = 0

# for event in pygame.event.get():
#     if event.type == MOUSEBUTTONDOWN:  #Better to seperate to a new if statement aswell, since there's more buttons that can be clicked and makes for cleaner code.
#         if event.button == 1:
#             for object in clickableObjectsList:
#                 object.clickCheck(event.pos)

# blueval = 0
# bluedir  = 1
LEFT = 1
x = y = 0
while (True):

   # check for quit events
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();
        elif event.type == pygame.MOUSEMOTION:
            # print("mouse at (%d, %d)" % event.pos)
            x, y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            x, y = event.pos
            for state in state_borders:
                if is_in_polygon(x, y, state_borders[state]):
                    # print("You pressed the left mouse button at (%d, %d)" % event.pos)
                    myfont = pygame.font.SysFont("monospace", 50)
                    pygame.draw.polygon(screen, red, state_borders[state])
                    #pygame.transform.scale2x(state_borders[state])
                    label = myfont.render(state, 1, blue)
                    screen.blit(label, random.choice(state_borders[state]))
                    #screen.blit(pygame.draw.polygon(scree))
                    #print(random.choice(state_borders[state]))
                    print("You pressed the left mouse button in " + state)
                    pygame.display.update()
                    pygame.time.wait(1000)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            x, y = event.pos
            for state in state_borders:
                if is_in_polygon(x, y, state_borders[state]):
                    # print("You released the left mouse button at (%d, %d)" % event.pos)
                    print("You released the left mouse button in " + state)

   # erase the screen
   #screen.fill(white)
   screen.blit(background, (0, 0))
   #pygame.draw.line(screen, red, (x, 0), (x, 1499))
   #pygame.draw.line(screen, red, (0, y), (1499, y))
   # blueval += bluedir
   # if blueval == 255 or blueval == 0:
   #     bluedir *= -1

   # draw the updated picture

   #updatePoints(points)  # changes the location of the points
   for state in state_borders:
       #subscreen = pygame.display.set_mode((100, 100))
       pygame.draw.polygon(screen,white,state_borders[state])
       pygame.draw.polygon(screen,black,state_borders[state], 1)
       #print(state_borders[state])
       # redraw the points
       #subscreen.fill(red)

   for hospital in hospitals:
       pygame.draw.circle(screen, green, hospitals[hospital], 1)
   # update the screen
   pygame.display.update()
