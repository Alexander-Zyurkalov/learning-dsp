from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.plotting import figure

from data import Data
from sliders import FrequencySlider, SamplesSlider, SamplingFrequencySlider, TimeSlider, ParameterSelectNyquist

data = Data()

# Create a new plot with a single line (the 'hand')
hand = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1), title='Magnitude and Phase')
hand.line('x', 'y', line_width=2, source=data.magnitude_and_phase)

compl = figure(width=400, height=400, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2), title='Complex y(n)')
compl.line('x', 'y', line_width=2, source=data.complex_original_signal)

# Create the new plots
p1 = figure(width=1500, height=400,  y_range=(-1.2, 1.2), title='Plot 1')
p2 = figure(width=1500, height=400,  y_range=(-1.2, 1.2), title='Plot 2')

colors = ['red', 'green', 'blue', 'indigo', 'orange', 'yellow']

checkbox_columns = [[], []]  # separate checkbox list for each figure

# Iterate over the signal groups
for group_name, signals in data.signal_groups.items():

    # Iterate over the signals in each group
    for index, (signal_name, source) in enumerate(signals.items()):
        # Pick a color from the list
        color = colors[index % len(colors)]

        # Add a line for each signal on each plot
        line1 = p1.line('x', 'y', source=source, color=color, legend_label=signal_name)
        line2 = p2.line('x', 'y', source=source, color=color, legend_label=signal_name)

        # Add a checkbox for each line in each figure
        checkbox1 = CheckboxGroup(labels=[signal_name], active=[0], width=150)
        checkbox2 = CheckboxGroup(labels=[signal_name], active=[0], width=150)

        # Attach a callback to each checkbox to control the visibility of the corresponding lines
        callback1 = CustomJS(args=dict(line=line1, checkbox=checkbox1), code="""
            line.visible = checkbox.active.includes(0);
        """)
        checkbox1.js_on_change('active', callback1)

        callback2 = CustomJS(args=dict(line=line2, checkbox=checkbox2), code="""
            line.visible = checkbox.active.includes(0);
        """)
        checkbox2.js_on_change('active', callback2)

        # Add the checkbox to the list
        checkbox_columns[0].append(checkbox1)
        checkbox_columns[1].append(checkbox2)

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

# Arrange the plots, the slider and the checkboxes in a layout
layout = column(
    frequency_slider.slider,
    row(
        column(
            samples_slider.slider,
            time_slider.slider,
            sampling_frequency_slider.slider,
            select_nyquist.select,
        ),
        row(hand, compl)
    ),
    column(
        row(column(*checkbox_columns[0])),
        p1,
        row(column(*checkbox_columns[1])),
        p2
    ),
)

# Update data and add root
data.update_data()
curdoc().add_root(layout)
