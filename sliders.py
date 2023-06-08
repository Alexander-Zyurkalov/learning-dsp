# Base class
from abc import abstractmethod, ABC

from bokeh.models import Slider


# Base class
class ParameterSlider(ABC):
    def __init__(self, data, start, end, value, step, title):
        self.data = data
        self.slider = Slider(start=start, end=end, value=value, step=step, title=title)
        self.slider.on_change('value', self.update)

    @abstractmethod
    def update(self, attrname, old, new):
        pass


# Frequency class
class FrequencySlider(ParameterSlider):
    def update(self, attrname, old, new):
        self.data.f = self.slider.value
        self.data.update_data()


# Samples class
class SamplesSlider(ParameterSlider):
    def __init__(self, data, start, end, value, step, title):
        super().__init__(data, start, end, value, step, title)
        self.time_slider = None

    def update(self, attrname, old, new):
        self.data.N = int(self.slider.value)
        self.data.s = self.data.N * self.data.T  # Modify s based on the new N
        self.data.update_data()
        if self.time_slider is not None:
            self.time_slider.slider.value = self.data.s

    def add_time_slider(self, time_slider):
        self.time_slider = time_slider


# Time class
class TimeSlider(ParameterSlider):
    def __init__(self, data, start, end, value, step, title, samples_slider: SamplesSlider):
        super().__init__(data, start, end, value, step, title)
        self.samples_slider = samples_slider

    def update(self, attrname, old, new):
        self.data.s = self.slider.value
        self.data.N = int(self.data.s / self.data.T)  # Modify N based on the new s
        if self.samples_slider is not None:
            self.samples_slider.slider.value = self.data.N
        self.data.update_data()


# Sampling frequency class
class SamplingFrequencySlider(ParameterSlider):
    def update(self, attrname, old, new):
        self.data.fs = self.slider.value
        self.data.T = 1.0 / self.data.fs  # Modify T based on the new fs
        self.data.update_data()

