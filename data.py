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


def calculated_y_one_sample_delayed(n, T, f):
    w = 2 * np.pi * f
    calculate_y = calculate_y_sine(n, T, f)
    delayed_y = np.zeros(n)
    for i in range(0, n):
        delayed_y[i] = calculate_y[i - 1]
    return delayed_y


def mix_with_delayed_sine(n, T, f):
    w = 2 * np.pi * f
    calculate_y = calculate_y_sine(n, T, f)
    delayed_y = np.zeros(n)
    for i in range(0, n):
        delayed_y[i] = 0.5 * calculate_y[i] + 0.5 * calculate_y[i - 1]
    return delayed_y


def transfer_function(f, T):
    w = 2 * np.pi * f
    return 0.5 + 0.5 * np.exp(-1j * w * T)


def magnitude_phase(H):
    magnitude = abs(H)
    phase = np.angle(H)
    return magnitude, phase


def delayed_ejnt(n, T, f):
    w = 2 * np.pi * f
    calculate_y = calculate_y_for_ewint(n, T, f)
    return calculate_y * np.exp(-1j * w * T)


def mixture_with_delayed_e_jnt(n, T, f):
    w = 2 * np.pi * f
    calculate_y = calculate_y_for_ewint(n, T, f)
    return calculate_y * transfer_function(f, T)


class Data:
    def __init__(self):
        self.f = 1
        self.N = 10
        self.fs = 10
        self.T = 1.0 / self.fs
        self.s = self.N * self.T

        # ColumnDataSource to hold the values
        self.magnitude_and_phase = ColumnDataSource(data=dict(x=[], y=[]))
        self.complex_original_signal = ColumnDataSource(data=dict(x=[], y=[]))

        self.signal_groups = {
            'e^{jnT}': {
                'real_signal': ColumnDataSource(data=dict(x=[], y=[])),
                'imag_signal': ColumnDataSource(data=dict(x=[], y=[])),
                'delayed_real_signal': ColumnDataSource(data=dict(x=[], y=[])),
                'delayed_imag_signal': ColumnDataSource(data=dict(x=[], y=[])),
                '0.5*original+0.5*delayed': ColumnDataSource(data=dict(x=[], y=[])),
                'real+imag':  ColumnDataSource(data=dict(x=[], y=[])),
            },
            'Sine': {
                'sine_original': ColumnDataSource(data=dict(x=[], y=[])),
                'sine_delayed': ColumnDataSource(data=dict(x=[], y=[])),
                'sine_mixed_with_delayed': ColumnDataSource(data=dict(x=[], y=[])),
            },
            'Impulse': {
                'impulse_original': ColumnDataSource(data=dict(x=[], y=[])),
                'impulse_delayed': ColumnDataSource(data=dict(x=[], y=[])),
                'impulse_mixed_with_delayed': ColumnDataSource(data=dict(x=[], y=[])),
            },
        }

        self.update_data()

    def update_data(self):
        # Function to calculate transfer function
        H = transfer_function(self.f, self.T)
        magnitude, phase = magnitude_phase(H)
        self.magnitude_and_phase.data = dict(x=[0, magnitude * np.cos(phase)], y=[0, magnitude * np.sin(phase)])

        y = calculate_y_for_ewint(self.N, self.T, self.f)
        self.complex_original_signal.data = dict(x=np.real(y), y=np.imag(y))

        mix_with_delayed = mixture_with_delayed_e_jnt(self.N, self.T, self.f)
        self.signal_groups['e^{jnT}']['real_signal'].data = dict(x=np.arange(self.N), y=np.real(y))
        self.signal_groups['e^{jnT}']['imag_signal'].data = dict(x=np.arange(self.N), y=np.imag(y))
        self.signal_groups['e^{jnT}']['delayed_real_signal'].data = dict(x=np.arange(self.N),
                                                                    y=np.real(delayed_ejnt(self.N, self.T, self.f)))
        self.signal_groups['e^{jnT}']['delayed_imag_signal'].data = dict(x=np.arange(self.N),
                                                                    y=np.imag(delayed_ejnt(self.N, self.T, self.f)))
        self.signal_groups['e^{jnT}']['0.5*original+0.5*delayed'].data = dict(x=np.arange(self.N),
                                                                              y=np.real(mix_with_delayed))
        self.signal_groups['e^{jnT}']['real+imag'].data = dict(x=np.arange(self.N), y=np.real(y) + np.imag(y))

        sine_y = calculate_y_sine(self.N, self.T, self.f)
        sine_mixed_with_delayed = mix_with_delayed_sine(self.N, self.T, self.f)
        self.signal_groups['Sine']['sine_original'].data = dict(x=np.arange(self.N), y=sine_y)
        self.signal_groups['Sine']['sine_delayed'].data = dict(x=np.arange(self.N),
                                                               y=calculated_y_one_sample_delayed(self.N, self.T,
                                                                                                 self.f))
        self.signal_groups['Sine']['sine_mixed_with_delayed'].data = dict(x=np.arange(self.N),
                                                                          y=sine_mixed_with_delayed)

        impulse_y = np.zeros(self.N)
        impulse_y[5] = 1

        delayed_impulse = np.zeros(self.N)
        delayed_impulse[6] = impulse_y[5]

        impulse_mixed_with_delayed = 0.5 * impulse_y + 0.5 * delayed_impulse

        self.signal_groups['Impulse']['impulse_original'].data = dict(x=np.arange(self.N), y=impulse_y)
        self.signal_groups['Impulse']['impulse_delayed'].data = dict(x=np.arange(self.N),
                                                                     y=delayed_impulse)
        self.signal_groups['Impulse']['impulse_mixed_with_delayed'].data = dict(x=np.arange(self.N),
                                                                                y=impulse_mixed_with_delayed)
