from bokeh.layouts import column
from bokeh.models import Slider
from bokeh.plotting import ColumnDataSource, show
from bokeh.plotting import figure
from bokeh.io import curdoc
import numpy as np

# Define initial parameters
target_v = 10.0
lp_initial = 0.1
num_steps = 500

# Define function to calculate v values
def calculate_values(target_v, lp, num_steps):
    v_values = np.zeros(num_steps)
    v = 0.0  # initial value
    lpinv = 1.0 - lp

    for i in range(num_steps):
        v = v * lpinv + target_v * lp
        v_values[i] = v

    return v_values

# Calculate initial data
x = np.arange(num_steps)
y = calculate_values(target_v, lp_initial, num_steps)

# Set up data source for plots
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(width=400, height=400, x_range=(0, num_steps), y_range=(0, target_v),
              title="v over time", tools="pan,reset,save,wheel_zoom,xbox_select", active_drag="xbox_select")
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up lp slider
lp_slider = Slider(start=0.0, end=0.1, value=lp_initial, step=0.0001, title="lp value", width=800)

# Set up callback for slider
def callback(attr, old, new):
    lp_val = lp_slider.value
    lpinv = 1.0 - lp_val
    v = 0.0
    y = []

    for i in range(num_steps):
        v = v * lpinv + target_v * lp_val
        y.append(v)

    source.data = dict(x=x, y=y)

# Connect slider to callback
lp_slider.on_change('value', callback)

# Arrange plots and widgets in layout
layout = column(lp_slider, plot)

# Add layout to curdoc
curdoc().add_root(layout)
