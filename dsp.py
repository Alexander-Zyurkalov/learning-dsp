import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Define the sampling rate (in Hz)
sampling_rate = 10000


f = 10
n_cyl = 5

# Generate the x-axis values (frequencies)
t = np.arange(start=0, stop=n_cyl * 1 / f - 1 / sampling_rate, step=1 / sampling_rate)
print(t)

# Generate the y-axis values (amplitudes) for the Nyquist frequency
y = np.sin(2 * np.pi * f * t)

# Create the plot
plt.plot(t, y)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Nyquist Frequency')
plt.grid(True)
plt.show()
