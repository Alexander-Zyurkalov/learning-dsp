from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
import numpy as np

# Function to calculate transfer function
def transfer_function(w):
    return 0.5 + 0.5 * np.exp(-1j * w)

# Initial value
w = 0
H = transfer_function(w)

# ColumnDataSource to hold the values
source = ColumnDataSource(data=dict(x=[H.real], y=[H.imag]))

# Create a new plot with a single point (the 'hand')
p = figure(width=400, height=400, x_range=(-1,1), y_range=(-1,1), title='Magnitude and Phase')
p.circle('x', 'y', size=10, source=source)

# Slider to control the frequency
frequency = Slider(start=-np.pi, end=np.pi, value=w, step=0.01, title="w")

# Update function to update the values when the slider changes
def update(attrname, old, new):
    w = frequency.value
    H = transfer_function(w)
    source.data = dict(x=[H.real], y=[H.imag])

frequency.on_change('value', update)

# Arrange the plot and the slider in a column
layout = column(frequency, p)

curdoc().add_root(layout)
