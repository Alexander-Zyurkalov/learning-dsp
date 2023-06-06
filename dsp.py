from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
import numpy as np

# Function to calculate transfer function
def transfer_function(w):
    return 0.5 + 0.5 * np.exp(-1j * w)

# Function to calculate magnitude and phase from a complex number
def magnitude_phase(H):
    magnitude = abs(H)
    phase = np.angle(H)
    return magnitude, phase

# Initial value
w = 0
H = transfer_function(w)
magnitude, phase = magnitude_phase(H)

# ColumnDataSource to hold the values
source = ColumnDataSource(data=dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)]))

# Create a new plot with a single line (the 'hand')
p = figure(width=400, height=400, x_range=(-1,1), y_range=(-1,1), title='Magnitude and Phase')
p.line('x', 'y', line_width=2, source=source)

# Slider to control the frequency
frequency_slider = Slider(start=-np.pi, end=np.pi, value=w, step=0.01, title="w")

# Update function to update the values when the slider changes
def update(attrname, old, new):
    w = frequency_slider.value
    H = transfer_function(w)
    magnitude, phase = magnitude_phase(H)
    source.data = dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)])

frequency_slider.on_change('value', update)

# Arrange the plot and the slider in a column
layout = column(frequency_slider, p)

curdoc().add_root(layout)
