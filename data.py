from bokeh.models import ColumnDataSource
import numpy as np


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

        self.update_data()

    def update_data(self):
        # Function to calculate y values
        y = self.calculate_y(self.N, self.T, self.f)

        # Function to calculate transfer function
        H = self.transfer_function(self.f)
        magnitude, phase = self.magnitude_phase(H)
        self.magnitude_and_phase.data = dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)])

        # Update the y(n) plot
        self.original_signal.data = dict(x=np.arange(self.N), y=np.real(y))

        # Update the complex y(n) plot
        self.complex_original_signal.data = dict(x=np.real(y), y=np.imag(y))

    # Function to calculate y values
    def calculate_y(self, n, T, f):
        if -0.01 < f < 0.01:
            f = 0
            # ones = np.ones(n)
            # ones[0] = 0
            # return ones * 1j
        # else:
        w = 2 * np.pi * f
        return np.exp(1j * w * np.arange(n) * T)

    # Function to calculate transfer function
    def transfer_function(self, f):
        w = 2 * np.pi * f
        return 0.5 + 0.5 * np.exp(-1j * w)

    # Function to calculate magnitude and phase from a complex number
    def magnitude_phase(self, H):
        magnitude = abs(H)
        phase = np.angle(H)
        return magnitude, phase
