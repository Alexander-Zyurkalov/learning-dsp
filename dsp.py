from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
import numpy as np

from data import Data
from sliders import FrequencySlider, SamplesSlider, SamplingFrequencySlider, TimeSlider



data = Data()

# Create a new plot with a single line (the 'hand')
p1 = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1), title='Magnitude and Phase')
p1.line('x', 'y', line_width=2, source=data.source1)

p2 = figure(width=1500, height=400, title='y(n)')
p2.line('x', 'y', source=data.source2)


# Create sliders
frequency_slider = FrequencySlider(data, start=-20, end=20, value=data.f, step=0.001, title="f")
samples_slider = SamplesSlider(data, start=1, end=100, value=data.N, step=1, title="N")
sampling_frequency_slider = SamplingFrequencySlider(data, start=1, end=100, value=data.fs, step=1, title="fs")
time_slider = TimeSlider(data, start=0.5, end=20, value=data.s, step=0.1, title="s")

# Arrange the plot and the slider in a column
layout1 = column(p1)
layout2 = column(samples_slider.slider, sampling_frequency_slider.slider, time_slider.slider, p2)

data.update_data()

layout = row(layout1, layout2)
curdoc().add_root(frequency_slider.slider)
curdoc().add_root(layout)
