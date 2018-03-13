
# coding: utf-8

# In[1]:


from Model import Model
import pandas as pd
from bokeh.io import output_file, show
from bokeh. plotting import figure, ColumnDataSource, curdoc
from bokeh.models import WMTSTileSource, HoverTool, CustomJS, Slider, ColumnDataSource
from bokeh.layouts import widgetbox, layout
import pickle
# from bokeh.models.widgets import TextInput


# In[2]:


# test = Model(12790, 12805)
# print(test)


# In[3]:


hurricanes = []
with open('hurricane_data.pkl', 'rb') as f:
    for _ in range(pickle.load(f)):
        hurricanes.append(pickle.load(f))


# output_file("slider.html")

# USA = x_range,y_range = ((-13884029,-7453304), (2698291,6455972))
bound = 20000000 # meters

p = figure(tools=['hover', 'pan', 'wheel_zoom'], x_range=(-bound, bound), y_range=(-bound, bound))
p.axis.visible = False

url = 'http://a.basemaps.cartocdn.com/dark_all/{Z}/{X}/{Y}.png'
attribution = "Tiles by Carto, under CC BY 3.0. Data by OSM, under ODbL"

p.add_tile(WMTSTileSource(url=url, attribution=attribution))

xs_array = []
ys_array = []
x_array = []
y_array = []
name_array =[]
season_array = []


for elm in hurricanes:
    for tempx in elm.x:
        xs_array.append(elm.x)
        x_array.append(tempx)
        name_array.append(elm.name)
        ys_array.append(elm.y)
        season_array.append(elm.season)
    for tempy in elm.y:
        y_array.append(tempy)

d = {'xs':xs_array, 'ys':ys_array, 'x':x_array, 'y':y_array, 'name':name_array, 'season':season_array}
df = pd.DataFrame(data=d)


source = ColumnDataSource(df[df.season == '1842'])


p.multi_line('xs', 'ys', source=source, color='firebrick', line_width = 3)
circle = p.circle('x','y', source=source, color='firebrick', size=10)

p.tools[0].renderers.append(circle)

# callback = CustomJS(args=dict(source=source), code="""
#         var data = source.data;
#         var ref = ref.value.toString()
#         var seas = data['season']
#         var color = data['color']
#         var alpha = data['alpha']
#         for(i=0; i<seas.length; i++){
#             if(seas[i] == ref){
#                 color[i] = "firebrick"
#                 alpha[i] = 1
#             }
#             else{
#                 color[i] = "whitesmoke"
#                 alpha[i] = 0
#             }
#         }
#         source.change.emit();
#     """)

def callback(attr, old, new):
    N = slider.value
    print(N)
    new1 = ColumnDataSource(df[df.season == str(N)])
    source.data = new1.data

#  had to install flexx

N=1842

slider = Slider(start=1842, end=2017, value=N, step=1, title="Season")
# callback.args["ref"] = slider
slider.on_change('value', callback)

# text_input = TextInput(value="2016", title="Label:")
# callback.args["val"] = text_input

hover = p.select(dict(type=HoverTool))
# hover = HoverTool()
hover.tooltips = [("Name", "@name"),("Season", "@season"), ("(x,y)", "($x, $y)")]
hover.mode = 'mouse'

# l = layout([widgetbox(slider, text_input), p])
l = layout([widgetbox(slider), p])
curdoc().add_root(l)
# show(l)
