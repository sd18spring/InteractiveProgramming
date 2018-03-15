"""Map.py takes in the information from the other python files and uses Bokeh to display the data in an interactive
way. The key bokeh features involve hovers, a slider, and a map. The script needs to be run using the bokeh server
because callback functions in CustomJS do not support the formation of new ColumnDataSources. (If you know of a way
to output the map as an html without using the bokeh server please email cassandra.overney@students.olin.edu.) For
now, you can run the file by typing "bokeh serve --show Map.py" in the terminal. It will take a few minutes to get
the map to appear. Make sure to have the pandas, bokeh, and pickle libraries installed before running. """

import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import WMTSTileSource, HoverTool, Slider, ColumnDataSource
from bokeh.layouts import widgetbox, layout
import pickle

# reads in the pickle file from the Model class and stores the hurricane objects into a simple array
hurricanes = []
with open('hurricane_data.pkl', 'rb') as f:
    for _ in range(pickle.load(f)):
        hurricanes.append(pickle.load(f))

# makes more arrays for the DataFrame and ColumnDataSource bokeh objects. Each array contains pertinent information
# for each hurricane. The arrays need to be the same length, so there are a lot of duplicates.
xs_array = []  # an array with each element being an array of x points in a hurricane's path (used for multi line)
ys_array = []  # an array with each element being an array of y points in a hurricane's path (used for multi line)
x_array = []  # an array with each element being a x coordinate of a hurricane's path (used for circle)
y_array = []  # an array with each element being a y coordinate of a hurricane's path (used for circle)
name_array = []  # an array with each element being a name of a hurricane (used for hover)
season_array = []  # an array with each element being a season/yr of a hurricane (used for slider)
time_array = []  # an array with each element being the time of a hurricane (used for hover)
duration_array = []  # an array with each element being the duration of a hurricane (used for hover)
cat_array = []  # an array with each element being the category of a hurricane (used for hover and colors)
color_array = []  # an array with each element being the color of a hurricane point (used for multi line and circle)

# a dictionary of colors with keys being the possible category names and the values being their corresponding colors
colors = {"5": "firebrick", "4": "gold", "3": "lime", "2": "olive", "1": "aqua", "TS": "blue", "TD": "purple",
          "NA": "whitesmoke"}

# iterate through each hurricane and add its data to the arrays declared above
for elm in hurricanes:
    for i, tempx in enumerate(elm.x):
        xs_array.append(elm.x)
        x_array.append(tempx)
        name_array.append(elm.name)
        ys_array.append(elm.y)
        y_array.append(elm.y[i])
        season_array.append(elm.season)
        time_array.append(elm.time)
        duration_array.append(elm.duration)
        cat_array.append(elm.category)
        color_array.append(colors.get(elm.category))

# make a dictionary of all the arrays with the keys being the array names
d = {'xs': xs_array, 'ys': ys_array, 'x': x_array, 'y': y_array, 'name': name_array, 'season': season_array,
     'time': time_array, 'duration': duration_array, 'cat': cat_array, 'color': color_array}

# translate that dictionary into a DataFrame
df = pd.DataFrame(data=d)

# makes the first ColumnDataSource by extracting all the data from df that has a season equal to 1842 (initial value
# of slider)
source = ColumnDataSource(df[df.season == '1842'])

# creates all the bokeh components for the data visualization
bound = 20000000  # in meters

p = figure(tools=['hover', 'pan', 'wheel_zoom'], x_range=(-bound, bound), y_range=(-bound, bound))
p.axis.visible = False

# WMTSTileSource borrowed from online
url = 'http://a.basemaps.cartocdn.com/dark_all/{Z}/{X}/{Y}.png'
attribution = "Tiles by Carto, under CC BY 3.0. Data by OSM, under ODbL"
p.add_tile(WMTSTileSource(url=url, attribution=attribution))

# uses source to plot the hurricane points and paths associated with the value of the slider
p.multi_line('xs', 'ys', source=source, color='color', line_width=3)
circle = p.circle('x', 'y', source=source, color='color', size=10)
p.tools[0].renderers.append(circle)


# callback function for slider
def callback(attr, old, new):
    """
    Takes value of slider and replaces the data in source by extracting all the data from df with season equal to
    slider value
    :param attr: typical parameters for bokeh callback
    :param old: typical parameters for bokeh callback
    :param new: typical parameters for bokeh callback
    :return: none
    """
    N = slider.value
    new1 = ColumnDataSource(df[df.season == str(N)])
    source.data = new1.data


# creates slider and hover
slider = Slider(start=1842, end=2017, value=1842, step=1, title="Year")
slider.on_change('value', callback)

hover = p.select(dict(type=HoverTool))
hover.tooltips = [("Name", "@name"), ("Time", "@time"), ("Duration", "@duration"),
                  ("Category", "@cat")]
hover.mode = 'mouse'

# creates the layout and outputs it to the bokeh server
l = layout([widgetbox(slider), p])
curdoc().add_root(l)
