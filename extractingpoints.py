import json
import pygame, sys
from pygame.locals import *
import math
import random
import csv
from PIL import Image
from collections import defaultdict

'''Takes the latitude and longitudes of the state borders and stores them in point objects.'''

state_abb = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

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

#https://hifld-dhs-gii.opendata.arcgis.com/datasets/5eafb083e43a457b9810c36b2414d3d3_0?uiTab=table&geometry=110.215%2C9.449%2C72.949%2C74.683&filterByExtent=false
hospitals = {}
with open('Hospitals.csv', newline='') as csvfile:
    hospitaldata = csv.reader(csvfile)#, delimiter=' ')
    for hospital in hospitaldata:
        if len(hospital) > 4 and hospital[0][0] in numbers:
            lng = hospital[0]
            lat = hospital[1]
            name = hospital[4]
            hospitals[str(name)] = (get_x(4000, float(lng)), get_y(4000, 2300, float(lat)))

#https://www.census.gov/data/datasets/time-series/demo/saipe/model-tables.html
irs_agi = {} #key = state, value = (median AGI, mean AGI)
with open('irs.csv', newline='') as csvfile:
    irsdata = csv.reader(csvfile)#, delimiter=' ')
    for row in irsdata:
        if row[2] == '2015':
            state = row[1]
            irs_agi[state] = (row[11], row[12])

charge_data = {}
charge_data_list =[]

with open('result.csv', newline='') as csvfile:
    health_charge_data = csv.reader(csvfile)
    for row in health_charge_data:
        if row[8] in state_abb:
            state = state_abb[row[8]]
            #charge_data[state] = (row[1])
            #print((charge))
            charge = float(row[1])
            if state not in charge_data.keys():
                charge_data[state] = [charge]
            else:
                charge_data[state].append(charge)
            #charge_data[state] = charge_data.get(state, list()).append(charge)

            #charge_data[state] = charge_data[state].append(charge)

    for state in charge_data:
         charge_data[state] = sum(charge_data[state])/len(charge_data[state])
    #         #charge_data[state] = charge_data.get(state, 0) + float(row[1])
    #
            #charge_data[state] = (charge_data.get(state[0], 0) + charge, charge_data.get(state[1], 0) + 1)

            #charge_data[state] =
            #charge_amount


    #print(charge_data)
key_max = max(charge_data)
val_min = min(charge_data)
# print(key_max)
# print(charge_data[key_max])
# print(charge_data[val_min])
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
pale_blue = (199, 219, 249)
light_blue = (148, 187, 247)
blue = (48, 129, 255)
dark_blue = (0, 90, 232)
darker_blue = (0, 55, 142)

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
#                 object.clickCheck(event.pos
charge_data['Washington'] = 0.00
charge_data['West Virginia'] = 0.00
charge_data['Wisconsin'] = 0.00
charge_data['Wyoming'] = 0.00

for charge in charge_data:
    charge_data[charge] = round(charge_data[charge], 2)

charge_list = list(zip(charge_data.keys(), charge_data.values()))
# for x,y in charge_list:
#     charge_list[x,y] = (x, round(y, 2))
# print(charge_list)

the_image = pygame.Surface([500,500], pygame.SRCALPHA, 32)
the_image = the_image.convert_alpha()
the_image_size = the_image.get_rect()

#white, pale blue, light blue, blue, dark blue, darker blue
colors2 = [(255,255,255), (199, 219, 249), (148, 187, 247), (48, 129, 255), (0, 90, 232), (0, 55, 142)]

# print(charge_list)
# charge_list.sort(key=lambda x: x[1])
# print(charge_list)

#screen.blit(image, (1000, 0))
#blank_rect = pygame.Rect(0, 0, 500, 500)
#pygame.draw.rect(image, green, blank_rect)
#pygame.draw.polygon(image, green, state_borders['Michigan'])

def set_color(charge_list, colors2, i):
    bin_size = int(len(charge_list)/6)
    #for i in range(len(charge_list)):
    if i in range(0,bin_size):
        return white
    elif i in range(bin_size,2*bin_size):
        return pale_blue
    elif i in range(2*bin_size,3*bin_size):
        return light_blue
    elif i in range(3*bin_size,4*bin_size):
        return blue
    elif i in range(4*bin_size,5*bin_size):
        return dark_blue
    else: #i in range(5*bin_size+1,6*bin_size):
        return darker_blue


for state in state_borders:
    lats = []
    lngs = []
    #coordinate = np.matrix()
    for coord in state_borders[state]:
        lats.append(coord[0])
        lngs.append(coord[1])
    updated_borders = {}
    updated_borders_list = []
    for element in state_borders[state]:
        lat = element[0]
        lng = element[1]
        updated_borders_list.append((lat - min(lats), lng - min(lngs)))
    updated_borders[state] = updated_borders_list
    #pygame.draw.polygon(the_image, set_color(charge_list, colors2,i), updated_borders[state])
    #set_color(charge_list, colors2)
    pygame.draw.polygon(the_image, black, updated_borders[state], 2)
    pygame.image.save(the_image, state + '.png')
    #updated_borders.clear()
    #lats[:] = []
    #lngs[:] = []
    #updated_borders_list[:] = []
    the_image = pygame.Surface([500, 500], pygame.SRCALPHA, 32)
    the_image = the_image.convert_alpha()

legend = pygame.Surface((1100, 100))
legend.fill((218, 112, 214))

#print(hospitals)
# hospitals_by_state = {}
# #print(hospitals_by_state.items())
# for state in state_borders:
#     for hospital in hospitals:
#         if is_in_polygon(hospitals[hospital][0], hospitals[hospital][1], state_borders[state]):
#             if state not in hospitals_by_state.keys():
#                 hospitals_by_state[state] = [hospitals[hospital]]
#             else:
#                 hospitals_by_state[state] = hospitals_by_state[state].append(hospitals[hospital])
            # except:
            #     hospitals_by_state[state] = [hospitals[hospital]]
#print(hospitals_by_state)
#import numpy
# blueval = 0
# bluedir  = 1
button = pygame.Rect(250, 700, 90, 75)
LEFT = 1
x = y = 0
i = 0
while (True):

   # erase the screen
   #screen.fill(white)
   screen.blit(background, (0, 0))
   screen.blit(legend, (350, 900))
   legend_font = pygame.font.SysFont("notosansmonocjksc", 20)
   label1 = legend_font.render('$0.00 -', 1, darkBlue)
   label2 = legend_font.render('$6151.38', 1, darkBlue)
   label3 = legend_font.render('6163.50 -', 1, darkBlue)
   label4 = legend_font.render('$6417.63', 1, darkBlue)
   label5 = legend_font.render('$6431.03 -', 1, darkBlue)
   label6 = legend_font.render('$6721.25', 1, darkBlue)
   label7 = legend_font.render('$6733.80 -', 1, darkBlue)
   label8 = legend_font.render('$7054.44', 1, darkBlue)
   label9 = legend_font.render('$7061.26 -', 1, darkBlue)
   label10 = legend_font.render('$7376.79', 1, darkBlue)
   label11 = legend_font.render('$7696.40 -', 1, darkBlue)
   # label12 = legend_font.render('$9081.86', 1, blue)
   # label13 = legend_font.render('$9290.80', 1, blue)
   label12 = legend_font.render('$10982.04', 1, darkBlue)
   pygame.draw.rect(screen, white, (370, 910, 20, 20))
   screen.blit(label1, (355, 925))
   screen.blit(label2, (355, 955))
   pygame.draw.rect(screen, pale_blue, (570, 910, 20, 20))
   screen.blit(label3, (555, 925))
   screen.blit(label4, (555, 955))
   pygame.draw.rect(screen, light_blue, (770, 910, 20, 20))
   screen.blit(label5, (755, 925))
   screen.blit(label6, (755, 955))
   pygame.draw.rect(screen, blue, (970, 910, 20, 20))
   screen.blit(label7, (955, 925))
   screen.blit(label8, (955, 955))
   pygame.draw.rect(screen, dark_blue, (1170, 910, 20, 20))
   screen.blit(label9, (1155, 925))
   screen.blit(label10, (1155, 955))
   pygame.draw.rect(screen, darker_blue, (1370, 910, 20, 20))
   screen.blit(label11, (1355, 925))
   screen.blit(label12, (1355, 955))
   #pygame.draw.line(screen, red, (x, 0), (x, 1499))
   #pygame.draw.line(screen, red, (0, y), (1499, y))
   # blueval += bluedir
   # if blueval == 255 or blueval == 0:
   #     bluedir *= -1

   # draw the updated picture

   #updatePoints(points)  # changes the location of the points

   for state in state_borders:
       i = i
       color = set_color(charge_list, colors2, i)
       #subscreen = pygame.display.set_mode((100, 100))
       pygame.draw.polygon(screen,color,state_borders[state])
       # for hospital in hospitals_by_state[state]:
       #     pygame.draw.circle(screen, green, hospital, 1)
       pygame.draw.polygon(screen,black,state_borders[state], 1)
       i += 1
       #print(state_borders[state])
       # redraw the points
       #subscreen.fill(red)
   pygame.draw.rect(screen, green, button)
   button_label1 = legend_font.render('Hospital', 1, darkBlue)
   button_label2 = legend_font.render('Locations', 1, darkBlue)
   screen.blit(button_label1, (250, 710))
   screen.blit(button_label2, (250, 730))
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
                   pygame.draw.polygon(screen, red, state_borders[state], 2)
                   #pygame.transform.scale2x(state_borders[state])
                   label = myfont.render(state, 1, red)
                   screen.blit(label, random.choice(state_borders[state]))
                   red_cross = pygame.image.load('red_cross.jpg')
                   pygame.draw.rect(screen, black, (998, 0, 501, 501), 2)
                   red_cross = pygame.transform.scale(red_cross, (500, 500))
                   # individual_state = pygame.image.load(state + '.png')
                   # if state != 'Alaska':
                   #     individual_state = pygame.transform.scale(individual_state, (1500, 1500))
                   # screen.blit(individual_state, (1000, 0))
                   screen.blit(red_cross, (999, 1))
                   myfont = pygame.font.SysFont("monospace", 20, bold=True)
                   title_font = pygame.font.SysFont("notosansmonocjksc", 50)
                   label = title_font.render(state, 1, blue)
                   label2 = myfont.render('Median AGI: $' + irs_agi[state][0], 1, darkBlue)
                   label3 = myfont.render('Mean AGI: $' + irs_agi[state][1], 1, darkBlue)
                   label4 = myfont.render('Average Medicare Payment: $' + str(charge_data[state]), 1, darkBlue)
                   screen.blit(label, (((500 - label.get_rect().width)/2)+1000, 10))
                   screen.blit(label2, (((500 - label2.get_rect().width)/2)+1000, 90))
                   screen.blit(label3, (((500 - label3.get_rect().width)/2)+1000, 110))
                   screen.blit(label4, (((500 - label4.get_rect().width)/2)+1000,130))
                   #screen.blit(individual_state, (1000, 0))
                   #screen.blit(pygame.draw.polygon(scree))
                   #print(random.choice(state_borders[state]))
                   #print("You pressed the left mouse button in " + state)
                   pygame.display.update()
                   pygame.time.wait(3000)
           if button.collidepoint(event.pos):
               for hospital in hospitals:
                   pygame.draw.circle(screen, green, hospitals[hospital], 1)
               pygame.display.update()
               pygame.time.wait(3000)
           #for state in state_borders:
           #    if is_in_polygon(x, y, state_borders[state]):
                   # print("You released the left mouse button at (%d, %d)" % event.pos)
                   #print("You released the left mouse button in " + state)
   # for hospital in hospitals:
   #     pygame.draw.circle(screen, green, hospitals[hospital], 1)
   # screen.blit(image, (1000, 0))
   # blank_rect = pygame.Rect(0, 0, 500, 500)
   # pygame.draw.rect(image, green, blank_rect)
   # #pygame.draw.polygon(image, green, state_borders['Michigan'])
   # lats = []
   # lngs = []
   # #coordinate = np.matrix()
   # for coord in state_borders['Michigan']:
   #     lats.append(coord[0])
   #     lngs.append(coord[1])
   # updated_borders = {}
   # updated_borders_list = []
   # for element in state_borders['Michigan']:
   #     lat = element[0]
   #     lng = element[1]
   #     updated_borders_list.append((lat - min(lats), lng - min(lngs)))
   # updated_borders['Michigan'] = updated_borders_list
   # #pygame.draw.polygon(image, green, updated_borders['Michigan'])
   # image_size = image_size.inflate(1, 1)
   # pygame.transform.smoothscale(image, image_size.size)
   #screen.blit(pygame.transform.scale(image, (1000, 1000)))
   #pygame.draw.polygon(image, green, )
   #print(updated_borders)
   #print(min(lats))
   #print(min(lngs))

   # update the screen
   pygame.display.update()
   i = 0
