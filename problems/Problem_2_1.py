import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

def plot_clock(step, numberOfSteps):
    plt.figure(figsize=(6,6))

    # Calculate minutes, degree, and radians
    minutes = step * numberOfSteps
    degree = minutes * 6 - 180
    radians = np.deg2rad(degree)

    # Plot the unit circle
    circle = plt.Circle((0, 0), 1, color='b', fill=False)
    plt.gca().add_patch(circle)

    # Plot the red line
    plt.plot([0, np.cos(radians)], [0, np.sin(radians)], 'r-')

    # Set the aspect ratio and limits
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    plt.grid(True)
    plt.show()

# Create interactive sliders
step_slider = widgets.IntSlider(value=55, min=0, max=60, step=1, description='Step:')
numberOfSteps_slider = widgets.IntSlider(value=0, min=0, max=60, step=1, description='Num of Steps:')

# Display the interactive plot
widgets.interactive(plot_clock, step=step_slider, numberOfSteps=numberOfSteps_slider)
