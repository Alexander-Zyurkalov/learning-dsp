from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
import numpy as np
from bokeh.layouts import row

# Function to calculate y values
def calculate_y(n, T, w):
    return np.exp(1j * w * np.arange(n) * T)

# Function to calculate transfer function
def transfer_function(w):
    return 0.5 + 0.5 * np.exp(-1j * w)

# Function to calculate magnitude and phase from a complex number
def magnitude_phase(H):
    magnitude = abs(H)
    phase = np.angle(H)
    return magnitude, phase

# Initial value
N = 10
T = 1.0
w = 0
H = transfer_function(w)
y = calculate_y(N, T, w)

s = 0.5  # initial value for s

magnitude, phase = magnitude_phase(H)

# ColumnDataSource to hold the values
source1 = ColumnDataSource(data=dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)]))
source2 = ColumnDataSource(data=dict(x=np.arange(N), y=np.real(y)))
source3 = ColumnDataSource(data=dict(x=np.arange(int(s / T)), y=np.real(y[:int(s / T)])))

# Create a new plot with a single line (the 'hand')
p1 = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1), title='Magnitude and Phase')
p1.line('x', 'y', line_width=2, source=source1)

p2 = figure(width=1500, height=400, title='y(n)')
p2.line('x', 'y', source=source2)

p3 = figure(width=1500, height=400, title='y(n) for s seconds')
p3.line('x', 'y', source=source3)

# Slider to control the frequency
frequency_slider = Slider(start=-np.pi, end=np.pi, value=w, step=0.001, title="w")
samples_slider = Slider(start=1, end=100, value=N, step=1, title="N")
# Slider to control the sampling frequency
sampling_frequency_slider = Slider(start=1, end=100, value=10, step=1, title="fs")
# Slider to control the time
time_slider = Slider(start=0.5, end=20, value=s, step=0.1, title="s")

# Update function to update the values when the slider changes
def update(attrname, old, new):
    w = frequency_slider.value
    N = samples_slider.value
    fs = sampling_frequency_slider.value  # Get the value of fs from the slider
    s = time_slider.value  # Get the value of s from the slider

    T = 1.0 / fs  # Modify T based on the new fs

    H = transfer_function(w)
    magnitude, phase = magnitude_phase(H)
    source1.data = dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)])

    # Update the y(n) plot
    y = calculate_y(N, T, w)
    source2.data = dict(x=np.arange(N), y=np.real(y))

    # Update the y(n) for s seconds plot
    y3 = calculate_y(int(s / T), T, w)
    source3.data = dict(x=np.arange(int(s / T)), y=np.real(y3))

frequency_slider.on_change('value', update)
samples_slider.on_change('value', update)
sampling_frequency_slider.on_change('value', update)  # Add this line to update fs when the slider changes
time_slider.on_change('value', update)  # Add this line to update s when the slider changes

# Arrange the plot and the slider in a column
layout1 = column(frequency_slider, p1)
layout2 = column(samples_slider, sampling_frequency_slider, time_slider, p2, p3)

layout = row(layout1, layout2)
curdoc().add_root(layout)
