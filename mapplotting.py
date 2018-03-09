"""
Plots maps and data for interactive programing mini project

By Juan Carlos del Rio
"""

import geoplotlib
import gmplot
import numpy
import matplotlib

class PlottingLayer(object):

    def __init__(self, data):
        self.data = data

    def invalidate(self, proj):
        x, y = proj.lonlat_to_screen(self.data['lon'], self.data['lat'])
        self.painter = BatchPainter()
        self.painter.points(x, y)

    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        self.painter.batch_draw()

class Maps(object):
    def __init__(self,region,height,width):
        self.region = region
        self.height = height
        self.width = width

    def draw_map():
        thedata = geoplotlib.utils.read_csv('testcsv.csv')
        geoplotlib.add_layer(PlottingLayer(thedata))
        geoplotlib.show()

Maps.draw_map()
