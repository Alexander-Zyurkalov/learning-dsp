from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.plotting import figure

from data import Data
from sliders import FrequencySlider, SamplesSlider, SamplingFrequencySlider, TimeSlider, ParameterSelectNyquist

data = Data()

colors = ['red', 'green', 'blue', 'indigo', 'orange', 'yellow']

hand = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1), title='Magnitude and Phase')
# Create a new plot with a single line (the 'hand')
for index, (handDataName, magnitude_and_phase) in enumerate(data.magnitude_and_phase.items()):
    color = colors[index % len(colors)]
    hand.line('x', 'y', line_width=2, source=magnitude_and_phase, legend_label=handDataName, color=color,
              muted_color=color, muted_alpha=0.05)
hand.legend.click_policy = "mute"

compl = figure(width=400, height=400, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2), title='Complex y(n)')
compl.line('x', 'y', line_width=2, source=data.complex_original_signal)

# Create the new plots
p1 = figure(width=1500, height=400, y_range=(-1.2, 1.2), title='Plot 1')
p2 = figure(width=1500, height=400, y_range=(-1.2, 1.2), title='Plot 2')

checkbox_columns = {1: {}, 2: {}}  # separate checkbox dict for each figure

# Iterate over the signal groups
for group_name, signals in data.signal_groups.items():
    checkbox_columns[1][group_name] = []
    checkbox_columns[2][group_name] = []

    # Add a checkbox for each group
    group_checkbox1 = CheckboxGroup(labels=[group_name], active=[0], width=150)
    group_checkbox2 = CheckboxGroup(labels=[group_name], active=[0], width=150)

    checkbox_columns[1][group_name].append(group_checkbox1)
    checkbox_columns[2][group_name].append(group_checkbox2)

    # Iterate over the signals in each group
    for index, (signal_name, source) in enumerate(signals.items()):
        # Pick a color from the list
        color = colors[index % len(colors)]

        # Add a line for each signal on each plot
        line1 = p1.line('x', 'y', source=source, color=color, legend_label=signal_name, muted_color=color,
                        muted_alpha=0.05)
        line2 = p2.line('x', 'y', source=source, color=color, legend_label=signal_name, muted_color=color,
                        muted_alpha=0.05)

        # Attach a callback to each checkbox to control the visibility of the corresponding lines
        callback1 = CustomJS(args=dict(line=line1, group_checkbox=group_checkbox1), code="""
            line.visible = group_checkbox.active.includes(0);
            line.glyph.line_alpha = group_checkbox.active.includes(0);
        """)
        group_checkbox1.js_on_change('active', callback1)

        callback2 = CustomJS(args=dict(line=line2, group_checkbox=group_checkbox2), code="""
            line.visible = group_checkbox.active.includes(0);
            line.glyph.line_alpha = group_checkbox.active.includes(0);
        """)
        group_checkbox2.js_on_change('active', callback2)

p1.legend.click_policy = "mute"
p2.legend.click_policy = "mute"

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
    row(
        column(
            samples_slider.slider,
            time_slider.slider,
            sampling_frequency_slider.slider,
            select_nyquist.select,
        ),
        row(hand, compl)
    ),
    frequency_slider.slider,
    column(
        row(*[column(*v) for v in checkbox_columns[1].values()]),
        p1,
    ),
    column(
        row(*[column(*v) for v in checkbox_columns[2].values()]),
        p2,
    ),
)

# Update data and add root
data.update_data()
curdoc().add_root(layout)
