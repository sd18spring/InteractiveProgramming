import json
import pygame, sys
from pygame.locals import *
import math
import random
import csv
from PIL import Image

'''Takes the latitude and longitudes of the state borders and stores them in point objects.'''

class Point():
    '''Represents a point in 2-D space
    attributes:
    x, y

    methods:
    is_in_polygon
    __init__
    __str__
    to_pixel_coords
    '''

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def to_pixel_coords(self):
        x = float(self.x)
        y = float(self.y)
        return (x, y)

    #credit for following function (in slightly more general form) to: http://www.ariel.com.au/a/python-point-int-poly.html
    def is_in_polygon(self, points):
        # points = []
        # for pt in points_objects:
        #     points.append(pt.to_pixel_coords())
        n = len(points)
        inside = False
        px1, py1 = points[0]
        for i in range(1, n + 1):
            px2, py2 = points[i % n]
            if self.y > min(py1, py2):
                if self.y <= max(py1, py2):
                    if self.x <= max(px1, px2):
                        if py1 != py2:
                            xinters = (y-py1)*(px2-px1)/(py2-py1)+px1
                        if px1 == px2 or self.x <= xinters:
                            inside = not inside
            px1, py1 = px2, py2
        return inside

def get_x(width, lng):
    return int(round(math.fmod((width * (180.0 + lng) / 360.0), (1.5 * width))))

def get_y(width, height, lat):
    lat_rad = lat * math.pi / 180.0
    merc = 0.5 * math.log( (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)) )
    return int(round((height / 2) - (width * merc / (2 * math.pi))))

#https://www.census.gov/data/datasets/time-series/demo/saipe/model-tables.html
irs_agi = {} #key = state, value = (median AGI, mean AGI)
with open('irs.csv', newline='') as csvfile:
    irsdata = csv.reader(csvfile)#, delimiter=' ')
    for row in irsdata:
        if row[2] == '2015':
            state = row[1]
            irs_agi[state] = (row[11], row[12])

with open('states.json', 'r') as f:
    datastore = json.load(f)

numbers = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '-': 0}

#https://hifld-dhs-gii.opendata.arcgis.com/datasets/5eafb083e43a457b9810c36b2414d3d3_0?uiTab=table&geometry=110.215%2C9.449%2C72.949%2C74.683&filterByExtent=false
hospitals = {}
with open('Hospitals.csv', newline='') as csvfile:
    hospitaldata = csv.reader(csvfile)#, delimiter=' ')
    for hospital in hospitaldata:
        if len(hospital) > 4 and hospital[0][0] in numbers:
            lng = hospital[0]
            lat = hospital[1]
            name = hospital[4]
            hospitals[str(name)] = Point(get_x(4000, float(lng)), get_y(4000, 2300, float(lat)))

class State():
    '''
    Represents a US State
    attributes:
    name
    border_coord_list
    mean/median AGI

    methods:
    __init__
    __str__
    extract_lng_lat
    plot
    '''

    def __init__(self, name):
        self.name = name
        self.border_coord_list = [Point(coord['lng'], coord['lat']) for coord in datastore[self.name]["Coordinates"]]
        self.agi_tuple = irs_agi[self.name]

    def __str__(self):
        state = [self.name + ' has coordinates: ']
        for coord in self.border_coord_list:
            s = str(coord.to_pixel_coords())
            state.append(s)
        state.append(' and has AGI: ' + str(self.agi_tuple))
        return ' '.join(state)

    def extract_lng_lat(self):
        lng_lat = [(get_x(4000, coord.to_pixel_coords()[0]), get_y(4000, 2300, coord.to_pixel_coords()[1])) for coord in self.border_coord_list]
        return lng_lat

    def plot_state(self):
        pygame.draw.polygon(screen,white,self.extract_lng_lat())
        pygame.draw.polygon(screen,black,self.extract_lng_lat(), 1)

pygame.init()
size = (1500, 1500)
screen = pygame.display.set_mode(size)
background = pygame.image.load('USflag.png')
background = pygame.transform.scale(background, size)

state_objects = {}
for state in datastore:
    if state != 'Dist of Columbia':
        state_objects[state] = State(state)

#pygame.display.flip()
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

colors = {(255,0,0): 'red', (0,255,0): 'green', (0,0,255): 'blue', (0,0,128): 'darkBlue', (255,255,255): 'white', (0,0,0): 'black', (255,200,200): 'pink'}

the_image = pygame.Surface([500,500], pygame.SRCALPHA, 32)
the_image = the_image.convert_alpha()
the_image_size = the_image.get_rect()

for state in state_objects:
    lats = []
    lngs = []
    for coord in state_objects[state].extract_lng_lat():
        lats.append(coord[0])
        lngs.append(coord[1])
    updated_borders = {}
    updated_borders_list = []
    for element in state_objects[state].extract_lng_lat():
        lat = element[0]
        lng = element[1]
        updated_borders_list.append((lat - min(lats), lng - min(lngs)))
    updated_borders[state] = updated_borders_list
    pygame.draw.polygon(the_image, white, updated_borders[state])
    pygame.draw.polygon(the_image, black, updated_borders[state], 2)
    pygame.image.save(the_image, state + '.png')
    the_image = pygame.Surface([500, 500], pygame.SRCALPHA, 32)
    the_image = the_image.convert_alpha()

LEFT = 1
x = y = 0

while (True):

   # check for quit events
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            x, y = event.pos
            for state in state_objects:
                current_pos = Point(x, y)
                if current_pos.is_in_polygon( state_objects[state].extract_lng_lat()):
                    myfont = pygame.font.SysFont("monospace", 50)
                    pygame.draw.polygon(screen, red, state_objects[state].extract_lng_lat(), 2)
                    label = myfont.render(state, 1, blue)
                    screen.blit(label, random.choice(state_objects[state].extract_lng_lat()))
                    individual_state = pygame.image.load(state + '.png')
                    if state != 'Alaska':
                        individual_state = pygame.transform.scale(individual_state, (1500, 1500))
                    screen.blit(individual_state, (1000, 0))
                    myfont = pygame.font.SysFont("monospace", 20)
                    label = myfont.render(state, 1, blue)
                    label2 = myfont.render('Median AGI: $' + irs_agi[state][0], 1, blue)
                    label3 = myfont.render('Mean AGI: $' + irs_agi[state][1], 1, blue)
                    screen.blit(label, (1000, 10))
                    screen.blit(label2, (1000, 30))
                    screen.blit(label3, (1000, 50))
                    pygame.display.update()
                    pygame.time.wait(1000)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            x, y = event.pos

   # erase the screen
   screen.blit(background, (0, 0))

   # draw the updated picture

   #updatePoints(points)  # changes the location of the points
   for state in state_objects:
       state_objects[state].plot_state()

   for hospital in hospitals:
       pygame.draw.circle(screen, green, (int(hospitals[hospital].to_pixel_coords()[0]), int(hospitals[hospital].to_pixel_coords()[1])), 1)
   # update the screen
   pygame.display.update()
