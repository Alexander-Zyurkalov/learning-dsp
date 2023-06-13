from bokeh.models import ColumnDataSource
import numpy as np


# Function to calculate y values
def calculate_y_for_ewint(n, T, f):
    if -0.01 < f < 0.01:
        f = 0
    w = 2 * np.pi * f
    return np.exp(1j * w * np.arange(n) * T)


def calculate_y_sine(n, T, f):
    if n < 0:
        return 0
    w = 2 * np.pi * f
    return np.sin(w * np.arange(n) * T)


def delayed_y_for_sine(n, T, f):
    w = 2 * np.pi * f
    calculate_y = calculate_y_sine(n, T, f)
    delayed_y = np.zeros(n)
    for i in range(0, n):
        delayed_y[i] = 0.5 * calculate_y[i] + 0.5 * calculate_y[i - 1]
    return delayed_y


def transfer_function(f):
    w = 2 * np.pi * f
    return 0.5 + 0.5 * np.exp(-1j * w)


def magnitude_phase(H):
    magnitude = abs(H)
    phase = np.angle(H)
    return magnitude, phase


def delayed_y_for_e(n, T, f):
    w = 2 * np.pi * f
    calculate_y = calculate_y_for_ewint(n, T, f)
    return 0.5 * calculate_y + 0.5 * calculate_y * np.exp(-1j * w)


class Data:
    def __init__(self):
        self.f = 1
        self.N = 10
        self.fs = 10
        self.T = 1.0 / self.fs
        self.s = self.N * self.T

        # ColumnDataSource to hold the values
        self.magnitude_and_phase = ColumnDataSource(data=dict(x=[], y=[]))
        self.original_signal = ColumnDataSource(data=dict(x=[], y=[]))
        self.delayed_signal = ColumnDataSource(data=dict(x=[], y=[]))
        self.complex_original_signal = ColumnDataSource(data=dict(x=[], y=[]))
        self.sine_original = ColumnDataSource(data=dict(x=[], y=[]))
        self.sine_original_delayed = ColumnDataSource(data=dict(x=[], y=[]))

        self.update_data()

    def update_data(self):
        # Function to calculate y values
        y = calculate_y_for_ewint(self.N, self.T, self.f)

        # Function to calculate transfer function
        H = transfer_function(self.f)
        magnitude, phase = magnitude_phase(H)
        self.magnitude_and_phase.data = dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)])

        # Update the y(n) plot
        self.original_signal.data = dict(x=np.arange(self.N), y=np.real(y))

        # Update the complex y(n) plot
        self.complex_original_signal.data = dict(x=np.real(y), y=np.imag(y))

        # Update the delayed y(n) plot
        delayed_y = delayed_y_for_e(self.N, self.T, self.f)
        self.delayed_signal.data = dict(x=np.arange(self.N), y=np.real(delayed_y))

        # Update the sine plot
        sine_y = calculate_y_sine(self.N, self.T, self.f)
        self.sine_original.data = dict(x=np.arange(self.N), y=sine_y)

        # Update the delayed sine plot
        delayed_sine_y = delayed_y_for_sine(self.N, self.T, self.f)
        self.sine_original_delayed.data = dict(x=np.arange(self.N), y=delayed_sine_y)
