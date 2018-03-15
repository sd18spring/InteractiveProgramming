"""Sample code for `us_map.py`.

Author: Oliver Steele <oliver.steele@olin.edu>
License: MIT

Requirements:

    sudo pip install BeautifulSoup
    sudo pip install matplotlib
    sudo pip install svg.path
"""

import pygame
import sys
import matplotlib.path
import wold_map
import csv

#year that the data will be plotted for
year = '2016'
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (75, 75, 255)
GREEN = (75, 255, 75)
RED = (255, 50, 50)
GRAY = (127, 127, 127)
LIGHT_GRAY = (191, 191, 191)
countries=['AF','AL','DZ','AD','AO','AI','AG','AR','AM','AW','AU','AT','AZ','BS','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BA','BW','BR',
'VG','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','HK','CO','KM','CG','CD','CR','CI','HR','CU','CY','CZ','DK','DJ','DM','DO',
'EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','GA','GM','GE','DE','GH','GR','GL','GD','GP','GT','GN','GW','GY','HT',
'HN','HU','IS','IN','ID','IR','IQ','IE','IL','IT','JM','JP','JO','KZ','KE','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MK','MG','MW',
'MY','MV','ML','MT','MQ','MR','MU','YT','MX','MD','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI','NE','NG','NO','OM',
'PK','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','KN','LC','VC','ST','SA','SN','RS','SC','SL','SG','SK',
'SI','SB','SO','ZA','SS','ES','LK','SD','SR','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TO','TT','TN','TR','TM','TC','UG','UA','AE','GB','US',
'UY','UZ','VU','VE','VN','VI','EH','YE','ZM','ZW']
COUNTRY = 'AF'
width, height = 2000,2000

pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)


def point_in_polygon(pt, polygon):
    """Returns True iff `pt` is inside `polygon`.
    `polygon` is a list of tuples `(x, y)`."""

    return matplotlib.path.Path(polygon).contains_point(pt)

def find_magic(countries):
#for i in range(len(countries)):
    magic_numbers = []
    for i in range(len(countries)):
        with open('Internet_Users_percentofpop_2000_2016.csv', newline='') as InternetUse:
            internet = csv.DictReader(InternetUse)
            for row in internet:
                if countries[i] in row['Country Code']:
                    IU = row[year]
                    if IU == '':
                        IU = 0
                    else:
                        IU = float(IU)
                    country_name = row['Country Name']

        with open('GDP_PC.csv', newline='') as GDP:
            GNP = csv.DictReader(GDP)
            for row in GNP:
                if country_name == row['Country Name']:
                    gdp = row[year]
                    if gdp == '':
                        gdp = 0
                    else:
                        gdp = float(gdp)

        if float(IU) != float(0) and float(gdp) != float(0):
            magic_number = [IU/gdp]
            magic_numbers = magic_numbers + magic_number
        else:
            zero = [0]
            magic_numbers = magic_numbers + zero

    return magic_numbers

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another."""
    range_output = output_interval_end-output_interval_start
    range_input = input_interval_end-input_interval_start
    distance = val - input_interval_start
    remap = ((distance/range_input)*range_output)+output_interval_start
    return remap

def color_map(val,minimum, maximum):
    """Maps input values between max and min IU/gdp cofficients to an integer
    0-255,suitable for use as an RGB color code
    """
    color_code = remap_interval(val,minimum ,maximum, 0, 255)
    return int(color_code)

color_coefficients = find_magic(countries)
max_coeff = max(color_coefficients)
min_coeff = min(color_coefficients)

for i in range(len(countries)):
    # Draw the polygons for the state.
    for polygon in wold_map.countries[countries[i]]:
        # `polygon` points are tuples `(float, float)`. PyGame requires `(int, int)`.
        points = [(int(x), int(y)) for x, y in polygon]
        # Draw the interior
        number = color_map(color_coefficients[i],min_coeff,max_coeff)
        if number > 0:
            color = (0,0,number)
        else:
            color = RED
        pygame.draw.polygon(screen,color, points)
        # Draw the boundary
        pygame.draw.polygon(screen, BLACK, points, 1)
    pygame.display.flip()



last_mouse_in_state = False

while True:
    if any(event.type == pygame.QUIT for event in pygame.event.get()):
        sys.exit()

    for country in countries:
        # Is the mouse inside the state?
        mouse_in_state = any(point_in_polygon(pygame.mouse.get_pos(), polygon) for polygon in wold_map.countries[country])
        # Only print a message if the mouse moved from the inside to the outside, or vice versa
        if mouse_in_state != last_mouse_in_state:
            last_mouse_in_state = mouse_in_state
            if mouse_in_state:
                print ('mouse in',country)
