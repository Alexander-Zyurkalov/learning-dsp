from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure

from data import Data
from sliders import FrequencySlider, SamplesSlider, SamplingFrequencySlider, TimeSlider

data = Data()

# Create a new plot with a single line (the 'hand')
p1 = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1), title='Magnitude and Phase')
p1.line('x', 'y', line_width=2, source=data.magnitude_and_phase)

p3 = figure(width=400, height=400, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2), title='Complex y(n)')
p3.line('x', 'y', line_width=2, source=data.complex_original_signal)

# Assuming you have two data sources: source2 and source3
p2 = figure(width=1500, height=400, title='e^inT', y_range=(-1.2, 1.2))
p2.line('x', 'y', source=data.original_signal, color='blue', legend_label="Real part of the signal")
p2.line('x', 'y', source=data.delayed_signal, color='red', legend_label="Delayed real part of the signal")

p4 = figure(width=1500, height=400, title='sine(wnT)', y_range=(-1.2, 1.2))
p4.line('x', 'y', source=data.sine_original, color='blue')

# Create sliders
frequency_slider = FrequencySlider(data, start=-5, end=20, value=data.f, step=0.005, title="f")
samples_slider = SamplesSlider(data, start=1, end=100, value=data.N, step=1, title="N")
time_slider = TimeSlider(data, start=0.5, end=20, value=data.s, step=0.1, title="s", samples_slider=samples_slider)
samples_slider.add_time_slider(time_slider)
sampling_frequency_slider = SamplingFrequencySlider(data, start=1, end=100, value=data.fs, step=1, title="fs",
                                                    samples_slider=samples_slider)

# Arrange the plot and the slider in a column
layout1 = column(p1, p3)
layout2 = column(
    samples_slider.slider, sampling_frequency_slider.slider, time_slider.slider,
    p2, p4)

data.update_data()

layout = row(layout1, layout2)
curdoc().add_root(frequency_slider.slider)
curdoc().add_root(layout)
