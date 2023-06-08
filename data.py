from bokeh.models import ColumnDataSource, Slider
import numpy as np


class Data:
    def __init__(self):
        self.f = 0
        self.N = 10
        self.fs = 10
        self.s = 0.5
        self.T = 1.0

        # ColumnDataSource to hold the values
        self.source1 = ColumnDataSource(data=dict(x=[], y=[]))
        self.source2 = ColumnDataSource(data=dict(x=[], y=[]))
        self.source3 = ColumnDataSource(data=dict(x=[], y=[]))

        self.update_data()

    def update_data(self):
        # Function to calculate y values
        y = self.calculate_y(self.N, self.T, self.f)

        # Function to calculate transfer function
        H = self.transfer_function(self.f)
        magnitude, phase = self.magnitude_phase(H)
        self.source1.data = dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)])

        # Update the y(n) plot
        self.source2.data = dict(x=np.arange(self.N), y=np.real(y))

        # Update the y(n) for s seconds plot
        y3 = self.calculate_y(int(self.s / self.T), self.T, self.f)
        self.source3.data = dict(x=np.arange(int(self.s / self.T)), y=np.real(y3))

    # Function to calculate y values
    def calculate_y(self, n, T, f):
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
