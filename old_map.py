import geoplotlib
import pandas as pd
from geoplotlib.core import BatchPainter
from geoplotlib.layers import HotspotManager
from geoplotlib.utils import DataAccessObject, BoundingBox
from geoplotlib import layers as layers
import numpy as np

class LineLayer(layers.BaseLayer):
    """
    draws line connecting points in hurricane path
    """
    def __init__(self, data, num, color=None, point_size=2, linewidth=1, f_tooltip=None):

        self.data = data
        self.indexlst = num
        self.color = color
        if self.color is None:
            self.color = [255, 0, 0]
        self.point_size = point_size
        self.f_tooltip = f_tooltip
        self.linewidth = linewidth
        self.hotspots = HotspotManager()

    def invalidate(self, proj):
        """
        This method is called each time layers need to be redrawn, i.e. on zoom.
        Typically in this method a BatchPainter is instantiated and all the rendering is performed

        :param proj: the current Projector object
        """
        self.painter = BatchPainter()
        self.painter.set_color(self.color)

        x1, y1 = proj.lonlat_to_screen(self.data['lon'], self.data['lat'])
        self.painter.points(x1, y1, 2 * self.point_size, False)
        for i in self.indexlst:
            if i < len(self.data['lon']) - 1:
                x1 = self.data['lon'][i]
                y1 = self.data['lat'][i]
                x2 = self.data['lon'][i+1]
                y2 = self.data['lat'][i+1]
                x1, y1 = proj.lonlat_to_screen(x1, y1)
                x2, y2 = proj.lonlat_to_screen(x2, y2)
                self.painter.lines(x1, y1, x2, y2, width=self.linewidth)

        # print(type(self.data['lon']))
        # if self.data['lon'] < len(self.longlst) -1:
        #     x2, y2 = proj.lonlat_to_screen(self.longlst[self.data['lon']+1], self.latlst[self.data['lat']+1])
        #     self.painter.points(x2, y2, 2 * self.point_size, False)
        #     self.painter.lines(x1, y1, x2, y2, width=self.linewidth)

        if self.f_tooltip:
            for i in range(0, len(x1)):
                record = {k: self.data[k][i] for k in self.data.keys()}
                self.hotspots.add_rect(x1[i] - self.point_size, y1[i] - self.point_size,
                                       2 * self.point_size, 2 * self.point_size,
                                       self.f_tooltip(record))


    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        """
        This method is called at every frame, and typically executes BatchPainter.batch_draw()
        :param proj: the current Projector object
        :param mouse_x: mouse x
        :param mouse_y: mouse y
        :param ui_manager: the current UiManager
        """
        self.painter.batch_draw()
        picked = self.hotspots.pick(mouse_x, mouse_y)
        if picked:
            ui_manager.tooltip(picked)

    def bbox(self):
        """
        Return the bounding box for this layer
        """
        return BoundingBox.from_points(lons=self.data['lon'], lats=self.data['lat'])

    def on_key_release(self, key, modifiers):
        """
        Override this method for custom handling of keystrokes
        :param key: the key that has been released
        :param modifiers: the key modifiers
        :return: True if the layer needs to call invalidate
        """
        return False

df = pd.read_csv("simpdata.csv", low_memory=False)
names = df.dtypes.index
# print(names)
lat = df['Latitude_for_mapping'] #you can also use df['column_name']
long = df['Longitude_for_mapping']
# print("lat", (lat[0]))
# print("long", long)
numindex = np.arange(long.size)
# print(numlong)
# print(numlat)
lst = DataAccessObject({'lon': long, 'lat': lat})
# print(lst)
# lst = list(zip(lat[1:], long[1:]))
# geoplotlib.dot(lst)
# geoplotlib.layers.DotDensityLayer(lst)
# geoplotlib.add_layer(layers.DotDensityLayer(lst))
geoplotlib.add_layer(LineLayer(lst, numindex))
# geoplotlib.shapefiles('Allstorms.ibtracs_all_lines.v03r10.shp', color=[0,0,255])
geoplotlib.show()