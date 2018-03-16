import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import WMTSTileSource, HoverTool, Slider, ColumnDataSource
from bokeh.layouts import widgetbox, layout
import pickle

# run with: bokeh serve --show MVPv4.py

hurricanes = []
print("hello")
with open('hurricane_data_old.pkl', 'rb') as f:
    for _ in range(pickle.load(f)):
        hurricanes.append(pickle.load(f))

bound = 20000000  # meters

p = figure(tools=['hover', 'pan', 'wheel_zoom'], x_range=(-bound, bound), y_range=(-bound, bound))
p.axis.visible = False

url = 'http://a.basemaps.cartocdn.com/dark_all/{Z}/{X}/{Y}.png'
attribution = "Tiles by Carto, under CC BY 3.0. Data by OSM, under ODbL"

p.add_tile(WMTSTileSource(url=url, attribution=attribution))

xs_array = []
ys_array = []
x_array = []
y_array = []
name_array = []
season_array = []
time_array = []
duration_array = []
cat_array = []
color_array = []

colors = {"5": "firebrick", "4": "gold", "3": "lime", "2": "olive", "1": "aqua", "TS": "blue", "TD": "purple",
          "NA": "whitesmoke"}

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


d = {'xs': xs_array, 'ys': ys_array, 'x': x_array, 'y': y_array, 'name': name_array, 'season': season_array,
     'time': time_array, 'duration': duration_array, 'cat': cat_array, 'color': color_array}

df = pd.DataFrame(data=d)

source = ColumnDataSource(df[df.season == '1842'])

p.multi_line('xs', 'ys', source=source, color='color', line_width=3)
circle = p.circle('x', 'y', source=source, color='color', size=10)

p.tools[0].renderers.append(circle)

def callback(attr, old, new):
    N = slider.value
    new1 = ColumnDataSource(df[df.season == str(N)])
    source.data = new1.data


slider = Slider(start=1842, end=2017, value=1842, step=1, title="Season")
slider.on_change('value', callback)

hover = p.select(dict(type=HoverTool))
hover.tooltips = [("Name", "@name"), ("Time", "@time"), ("Duration", "@duration"),
                  ("Category", "@cat")]
hover.mode = 'mouse'

l = layout([widgetbox(slider), p])
curdoc().add_root(l)

