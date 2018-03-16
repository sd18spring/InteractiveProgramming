from bokeh.io import show
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import RdBu3
from bokeh.plotting import figure

source = ColumnDataSource(dict(
    x=[1, 2, 3, 4, 5, 6],
    y=[2, 1, 2, 1, 2, 1],
    label=['hi', 'lo', 'hi', 'lo', 'hi', 'lo']
))
color_mapper = CategoricalColorMapper(factors=['hi', 'lo'], palette=[RdBu3[2], RdBu3[0]])

p = figure(x_range=(0, 7), y_range=(0, 3), height=300, tools='save')
p.circle(
    x='x', y='y', radius=0.5, source=source,
    color={'field': 'label', 'transform': color_mapper},
    legend='label'
)
show(p)
