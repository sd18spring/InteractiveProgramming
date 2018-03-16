"""
Software Design Mini Project 4: Interactive Programming

@authors: Daniel Connolly and Jillian MacGregor

"""

import json
import pygame, sys
from pygame.locals import *
import math
import random
import csv

'''
The functions get_x and get_y are the formulae for converting coordinates from longitudes and latitudes to integer values using the Mercator Projection. The size of Alaska on our map is thus explained by the fact that we used the mercator projection to convert to pixel coordinates.
'''
def get_x(width, lng):
    return int(round(math.fmod((width * (180.0 + lng) / 360.0), (1.5 * width))))

def get_y(width, height, lat):
    lat_rad = lat * math.pi / 180.0
    merc = 0.5 * math.log( (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)) )
    return int(round((height / 2) - (width * merc / (2 * math.pi))))

#credit for following function to: http://www.ariel.com.au/a/python-point-int-poly.html
def is_in_polygon(x, y, points):
    '''
    Checks if a point (x, y) is within the area bounded by a list of coordinates (called points) that represent the borders of a polygon.
    '''
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

#The following are the RGB values for multiple colors.
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

#A dictionary representing alphanumeric characters that could be used to represent numbers (both positive and negative).
numbers = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '-': 0}

#A dictionary to convert from a state abbreviation to the actual state name.
state_abb = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

'''
Gets the coordinates for each point along the border of each state in the US and stores the results in a dictionary with values that are lists of tuples representing coordinates.
'''
state_borders = {}
all_points_list = []
with open('states.json', 'r') as f:
    datastore = json.load(f)
for state in datastore:
    points_list = []
    for coord in datastore[state]["Coordinates"]:
        points_list.append((get_x(4000, coord['lng']), get_y(4000, 2300, coord['lat'])))
    state_borders[state] = points_list

'''
Gets the locations of all of the registered hospitals in the United States and stores the locations in a dictionary.
'''
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

'''
Gets the median and mean adjusted gross income for each state and stores the values in a dictionary of tuples.
'''
#https://www.census.gov/data/datasets/time-series/demo/saipe/model-tables.html
irs_agi = {} #key = state, value = (median AGI, mean AGI)
with open('irs.csv', newline='') as csvfile:
    irsdata = csv.reader(csvfile)#, delimiter=' ')
    for row in irsdata:
        if row[2] == '2015':
            state = row[1]
            irs_agi[state] = (row[11], row[12])

'''
Gets the data regarding medicare payments for each state and creates a dictionary containing each state and the corresponding average medicare payment for that state.
'''
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

    for state in charge_data:
         charge_data[state] = sum(charge_data[state])/len(charge_data[state])

'''
Since there is no data regarding Medicare payments for these states in the file we used, we ensure that the program does not encounter errors by adding the following values to the dictionary.
'''
charge_data['Washington'] = 0.00
charge_data['West Virginia'] = 0.00
charge_data['Wisconsin'] = 0.00
charge_data['Wyoming'] = 0.00

'''
Truncates the average medicare payments to two decimal places.
'''
for charge in charge_data:
    charge_data[charge] = round(charge_data[charge], 2)

'''Turns the charge data dictionary into a list of tuples.'''
charge_list = list(zip(charge_data.keys(), charge_data.values()))

#List of the following colors: white, pale blue, light blue, blue, dark blue, darker blue
colors2 = [(255,255,255), (199, 219, 249), (148, 187, 247), (48, 129, 255), (0, 90, 232), (0, 55, 142)]

def set_color(charge_list, colors2, i):
    '''
    Sets the color of a state based upon its average medicare payment.
    '''
    bin_size = int(len(charge_list)/6)
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
    else:
        return darker_blue

if __name__ == '__main__':

    '''
    Initialized pygame, the screen, and creates a background Surface object.
    '''
    pygame.init()
    size = (1500, 1500)
    screen = pygame.display.set_mode(size)
    background = pygame.image.load('USflag.png')
    background = pygame.transform.scale(background, size)

    '''
    Creates a Rectangle object for the Hospital Locations button.
    '''
    button = pygame.Rect(250, 700, 90, 75)
    LEFT = 1
    x = y = 0
    i = 0

    '''
    Create a surface for the legend.
    '''
    legend = pygame.Surface((850, 100))
    legend.fill((218, 112, 214))

    while (True):

       '''
       Adds background image to the screen.
       '''
       screen.blit(background, (0, 0))
       pygame.draw.rect(screen, black, (346, 896, 858, 108))

       '''
       Creates legend to show relationship between the color of a state and its average medicare payment.
       '''
       screen.blit(legend, (350, 900))
       legend_font = pygame.font.SysFont("notosansmonocjksc", 20)
       label_legend = legend_font.render('State Color by Average Medicare Payment:', 1, darkBlue)
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
       label12 = legend_font.render('$10982.04', 1, darkBlue)
       screen.blit(label_legend, (346, 866))
       pygame.draw.rect(screen, white, (380, 910, 20, 20))
       screen.blit(label1, (355, 925))
       screen.blit(label2, (355, 955))
       pygame.draw.rect(screen, pale_blue, (530, 910, 20, 20))
       screen.blit(label3, (505, 925))
       screen.blit(label4, (505, 955))
       pygame.draw.rect(screen, light_blue, (680, 910, 20, 20))
       screen.blit(label5, (655, 925))
       screen.blit(label6, (655, 955))
       pygame.draw.rect(screen, blue, (830, 910, 20, 20))
       screen.blit(label7, (805, 925))
       screen.blit(label8, (805, 955))
       pygame.draw.rect(screen, dark_blue, (980, 910, 20, 20))
       screen.blit(label9, (955, 925))
       screen.blit(label10, (955, 955))
       pygame.draw.rect(screen, darker_blue, (1130, 910, 20, 20))
       screen.blit(label11, (1105, 925))
       screen.blit(label12, (1105, 955))

       # draw the updated picture
       '''
       Draws the states as polygons represented by a list of the pixel coordinates of their borders.
       '''
       for state in state_borders:
           i = i
           color = set_color(charge_list, colors2, i)
           pygame.draw.polygon(screen,color,state_borders[state])
           pygame.draw.polygon(screen,black,state_borders[state], 1)
           i += 1
       '''
       Draws the Hospital Locations button on the screen.
       '''
       pygame.draw.rect(screen, black, (246, 696, 98, 83))
       pygame.draw.rect(screen, green, button)
       button_label1 = legend_font.render('Hospital', 1, darkBlue)
       button_label2 = legend_font.render('Locations', 1, darkBlue)
       screen.blit(button_label1, (250, 710))
       screen.blit(button_label2, (250, 730))
       '''
       Checks for and handles mouse events.
       '''
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit(); sys.exit();
          elif event.type == pygame.MOUSEMOTION:
               x, y = event.pos
          elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
               x, y = event.pos
               for state in state_borders:
                   '''
                   If the controller clicks the mouse while over a state, healthcare and income data regarding that state is displayed.
                   '''
                   if is_in_polygon(x, y, state_borders[state]):
                       state_name_font = pygame.font.SysFont("tlwgtypewriter", 50, bold=True)
                       pygame.draw.polygon(screen, red, state_borders[state], 2)
                       label = state_name_font.render(state, 1, black)
                       screen.blit(label, random.choice(state_borders[state]))
                       red_cross = pygame.image.load('red_cross.jpg')
                       pygame.draw.rect(screen, black, (998, 0, 501, 501), 2)
                       red_cross = pygame.transform.scale(red_cross, (500, 500))
                       screen.blit(red_cross, (999, 1))
                       myfont = pygame.font.SysFont("monospace", 20, bold=True)
                       title_font = pygame.font.SysFont("notosansmonocjksc", 50)
                       label = title_font.render(state, 1, blue)
                       label2 = myfont.render('Median Adjusted Gross Income: $' + irs_agi[state][0], 1, darkBlue)
                       label3 = myfont.render('Mean Adjusted Gross Income: $' + irs_agi[state][1], 1, darkBlue)
                       label4 = myfont.render('Average Medicare Payment: $' + str(charge_data[state]), 1, darkBlue)
                       screen.blit(label, (((500 - label.get_rect().width)/2)+1000, 10))
                       screen.blit(label2, (((500 - label2.get_rect().width)/2)+1000, 120))
                       screen.blit(label3, (((500 - label3.get_rect().width)/2)+1000, 160))
                       screen.blit(label4, (((500 - label4.get_rect().width)/2)+1000,200))
                       pygame.display.update()
                       pygame.time.wait(3000)
               '''
               If the controller clicks the mouse while over the Hospital Locations button, the locations of all of the hospitals in the United States are displayed on the map.
               '''
               if button.collidepoint(event.pos):
                   for hospital in hospitals:
                       pygame.draw.circle(screen, green, hospitals[hospital], 1)
                   pygame.display.update()
                   pygame.time.wait(3000)

       # update the screen
       pygame.display.update()
       i = 0
    pygame.quit()
