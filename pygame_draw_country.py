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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
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
width, height = 2000, 2000

pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)


def point_in_polygon(pt, polygon):
    """Returns True iff `pt` is inside `polygon`.
    `polygon` is a list of tuples `(x, y)`."""

    return matplotlib.path.Path(polygon).contains_point(pt)

for country in countries:
    # Draw the polygons for the state.
    for polygon in wold_map.countries[country]:
        # `polygon` points are tuples `(float, float)`. PyGame requires `(int, int)`.
        points = [(int(x), int(y)) for x, y in polygon]
        # Draw the interior
        pygame.draw.polygon(screen, GREEN, points)
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
