from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.plotting import figure

from data import Data
from sliders import FrequencySlider, SamplesSlider, SamplingFrequencySlider, TimeSlider, ParameterSelectNyquist

data = Data()

# Create a new plot with a single line (the 'hand')
p1 = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1), title='Magnitude and Phase')
p1.line('x', 'y', line_width=2, source=data.magnitude_and_phase)

p3 = figure(width=400, height=400, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2), title='Complex y(n)')
p3.line('x', 'y', line_width=2, source=data.complex_original_signal)

colors = ['red', 'green', 'blue', 'indigo', 'orange', 'yellow']

# Create the figures in a loop
figure_list = []

for group_name, signals in data.signal_groups.items():
    checkbox_list = []
    p = figure(width=1500, height=400, title=group_name, y_range=(-1.2, 1.2))
    for index, (signal_name, source) in enumerate(signals.items()):
        # Pick a color from the list, cycling back to the start if there are more signals than colors
        color = colors[index % len(colors)]
        line = p.line('x', 'y', source=source, color=color, legend_label=signal_name)

        # Add a checkbox for each line
        checkbox = CheckboxGroup(labels=[signal_name], active=[0], width=150)

        # Attach a callback to each checkbox to control the visibility of the corresponding line
        callback = CustomJS(args=dict(line=line, checkbox=checkbox), code="""
            line.visible = checkbox.active.includes(0);
        """)
        checkbox.js_on_change('active', callback)

        # Add the checkbox to the list
        checkbox_list.append(checkbox)

    # Arrange each plot and its checkboxes in a column and add to the figure_list
    figure_list.append(column(p, *checkbox_list))



# Create sliders
frequency_slider = FrequencySlider(data, start=-5, end=20, value=data.f, step=0.005, title="f")
samples_slider = SamplesSlider(data, start=1, end=100, value=data.N, step=1, title="N")
time_slider = TimeSlider(data, start=0.5, end=20, value=data.s, step=0.1, title="s", samples_slider=samples_slider)
samples_slider.add_time_slider(time_slider)
sampling_frequency_slider = SamplingFrequencySlider(data, start=1, end=100, value=data.fs, step=1, title="fs",
                                                    samples_slider=samples_slider)
select_nyquist = ParameterSelectNyquist(data, frequency_slider)
sampling_frequency_slider.add_select(select_nyquist)
frequency_slider.add_select(select_nyquist)

# Arrange the plot and the slider in a column
layout1 = column(p1, p3)
layout2 = column(
    samples_slider.slider, sampling_frequency_slider.slider, time_slider.slider,
    *figure_list)

data.update_data()

layout = row(layout1, layout2)
curdoc().add_root(select_nyquist.select)
curdoc().add_root(frequency_slider.slider)
curdoc().add_root(layout)
