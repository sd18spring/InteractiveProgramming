import json
import pygame, sys
from pygame.locals import *
import math
import random
import csv
import time

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
        print(len(points))
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

    def get_mercator_projection(self, width, height):
        new_x = int(round(math.fmod((width * (180.0 + self.x) / 360.0), (1.5 * width))))
        lat_rad = self.y * math.pi / 180.0
        merc = 0.5 * math.log( (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)) )
        new_y = int(round((height / 2) - (width * merc / (2 * math.pi))))
        return Point(new_x, new_y)

    def get_merc_x(width, lng):
        return int(round(math.fmod((width * (180.0 + lng) / 360.0), (1.5 * width))))

    def get_merc_y(width, height, lat):
        lat_rad = lat * math.pi / 180.0
        merc = 0.5 * math.log( (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)) )
        return int(round((height / 2) - (width * merc / (2 * math.pi))))


class USHealthDataModel(object):
    """ Encodes a model of the data visualization state """
    def __init__(self, size, state_objects, hospitals, irs_agi):
        self.state_objects = state_objects
        # for state in datastore:
        #     if state != 'Dist of Columbia':
        #         self.state_objects[state] = State(state)
        self.hospitals = hospitals
        # for hospital in hospitaldata:
        #     if len(hospital) > 4 and hospital[0][0] in numbers:
        #         lng = hospital[0]
        #         lat = hospital[1]
        #         name = hospital[4]
        #         self.hospitals[str(name)] = Point(float(lng), float(lat)).get_mercator_projection(4000, 2300)
        self.irs_agi = irs_agi
        # for row in irsdata:
        #     if row[2] == '2015':
        #         state = row[1]
        #         irs_agi[state] = (row[11], row[12])
        self.colors = colors
        self.numbers = numbers

    def make_state_with_data(self, given_state):
        self.state_pic_surf = pygame.Surface([500,500], pygame.SRCALPHA, 32)
        self.state_pic_surf = self.state_pic_surf.convert_alpha()
        self.state_pic_surf_size = self.state_pic_surf.get_rect()
        lats = []
        lngs = []
        for coord in given_state.extract_lng_lat():
            # print(coord)
            lats.append(coord[0])
            lngs.append(coord[1])
        updated_borders = {}
        updated_borders_list = []
        for element in given_state.extract_lng_lat():
            lat = element[0]
            lng = element[1]
            updated_borders_list.append((lat - min(lats), lng - min(lngs)))
        updated_borders[given_state] = updated_borders_list
        pygame.draw.polygon(self.state_pic_surf, colors['white'], updated_borders[given_state])
        pygame.draw.polygon(self.state_pic_surf, colors['black'], updated_borders[given_state], 2)
        pygame.image.save(self.state_pic_surf, given_state.name + '.png')
        self.state_pic_surf = pygame.Surface([500, 500], pygame.SRCALPHA, 32)
        self.state_pic_surf = self.state_pic_surf.convert_alpha()


class State(USHealthDataModel):
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
        self.border_coord_list = [Point(coord['lng'], coord['lat']).get_mercator_projection(4000, 2300) for coord in datastore[self.name]["Coordinates"]]
        #self.border_coord_list = [(get_x(4000, coord['lng']), get_y(4000, 2300, coord['lat'])) for coord in datastore[self.name]["Coordinates"]]
        self.agi_tuple = irs_agi[self.name]

    def __str__(self):
        state = [self.name + ' has coordinates: ']
        for coord in self.border_coord_list:
            s = str(coord.to_pixel_coords())
            state.append(s)
        state.append(' and has AGI: ' + str(self.agi_tuple))
        return ' '.join(state)

    def extract_lng_lat(self):
        lng_lat = [(coord.to_pixel_coords()[0], coord.to_pixel_coords()[1]) for coord in self.border_coord_list]
        return lng_lat

    def plot_state(self):
        pygame.draw.polygon(screen,colors['white'],self.extract_lng_lat())
        pygame.draw.polygon(screen,colors['black'],self.extract_lng_lat(), 1)


class PyGameWindowView(object):
    """ A view of """
    def __init__(self, model, size):
        """ insert_here"""
        self.model = model
        self.size = size
        self.screen = screen
        #self.background = pygame.image.load('USflag.png')
        self.background = pygame.transform.scale(pygame.image.load('USflag.png'), size)

    def draw(self):
        """ Draw the current game state to the screen """
        #self.screen.fill(pygame.Color(0,0,0))
       # erase the screen
        self.screen.blit(self.background, (0, 0))

       # draw the updated picture

       #updatePoints(points)  # changes the location of the points
        for state in self.model.state_objects:
           self.model.state_objects[state].plot_state()

        for hospital in self.model.hospitals:
           pygame.draw.circle(screen, self.model.colors['green'], (int(self.model.hospitals[hospital].to_pixel_coords()[0]), int(self.model.hospitals[hospital].to_pixel_coords()[1])), 1)
       # update the screen
        pygame.display.update()

    def update_view(self, x, y):
        current_pos = Point(x, y)
        for state in self.model.state_objects:
            # current_pos = Point(x, y)
            if(current_pos.is_in_polygon(self.model.state_objects[state].extract_lng_lat())):
                print(current_pos)
                #print(state.name)
                print(self.model.state_objects[state].name)
                #print(self.model.state_objects[state].extract_lng_lat())
                self.model.make_state_with_data(self.model.state_objects[state])
                myfont = pygame.font.SysFont("monospace", 50)
                pygame.draw.polygon(self.screen, colors['red'], self.model.state_objects[state].extract_lng_lat(), 2)
                label = myfont.render(state, 1, colors['blue'])
                self.screen.blit(label, random.choice(self.model.state_objects[state].extract_lng_lat()))
                individual_state = pygame.image.load(state + '.png')
                if state != 'Alaska':
                    individual_state = pygame.transform.scale(individual_state, (1500, 1500))
                self.screen.blit(individual_state, (1000, 0))
                myfont = pygame.font.SysFont("monospace", 20)
                label = myfont.render(state, 1, self.model.colors['blue'])
                label2 = myfont.render('Median AGI: $' + self.model.irs_agi[state][0], 1, colors['blue'])
                label3 = myfont.render('Mean AGI: $' + self.model.irs_agi[state][1], 1, self.model.colors['blue'])
                self.screen.blit(label, (1000, 10))
                self.screen.blit(label2, (1000, 30))
                self.screen.blit(label3, (1000, 50))
                pygame.display.update()
                pygame.time.wait(100)
                break



class PyGameMouseController(object):
    """ A controller """
    def __init__(self,model, view):
        self.model = model
        self.view = view

    def handle_event(self,event):
        """ Handle the mouse event"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            x, y = event.pos
            # for state in self.model.state_objects:
            #     current_pos = Point(x, y)
            #     if current_pos.is_in_polygon( self.model.state_objects[state].extract_lng_lat()):
            self.view.update_view(x, y)

LEFT = 1
x = y = 0

if __name__ == '__main__':
    colors = {'red': (255,0,0), 'green': (0,255,0), 'blue': (0,0,255), 'darkBlue': (0,0,128), 'white':(255,255,255), 'black': (0,0,0), 'pink': (255,200,200)}
    numbers = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '-': 0}

    with open('irs.csv', newline='') as csvfile:
        irsdata = csv.reader(csvfile)#, delimiter=' ')
        irs_agi = {}
        for row in irsdata:
            if row[2] == '2015':
                state = row[1]
                irs_agi[state] = (row[11], row[12])
        # for row in irsdata:
        #     if row[2] == '2015':
        #         state = row[1]
        #         irs_agi[state] = (row[11], row[12])

    with open('states.json', 'r') as f:
        datastore = json.load(f)
        state_objects = {}
        for state in datastore:
            if state != 'Dist of Columbia':
                state_objects[state] = State(state)
            else:
                break
    with open('Hospitals.csv', newline='') as csvfile:
        hospitaldata = csv.reader(csvfile)#, delimiter=' ')
        hospitals = {}
        for hospital in hospitaldata:
            if len(hospital) > 4 and hospital[0][0] in numbers:
                lng = hospital[0]
                lat = hospital[1]
                name = hospital[4]
                hospitals[str(name)] = Point(float(lng), float(lat)).get_mercator_projection(4000, 2300)

    pygame.init()
    size = (1500, 1500)
    screen = pygame.display.set_mode(size)
    model = USHealthDataModel(size, state_objects, hospitals, irs_agi)
    view = PyGameWindowView(model, size)
    controller = PyGameMouseController(model, view)
    while (True):

       # check for quit events
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();
            controller.handle_event(event)
        #model.update()
       view.draw()
       # time.sleep(0.001)

    pygame.quit()
