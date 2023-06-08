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
    def update(self, attrname, old, new):
        self.data.N = int(self.slider.value)
        self.data.update_data()


# Sampling frequency class
class SamplingFrequencySlider(ParameterSlider):
    def update(self, attrname, old, new):
        self.data.fs = self.slider.value
        self.data.T = 1.0 / self.data.fs  # Modify T based on the new fs
        self.data.update_data()


# Time class
class TimeSlider(ParameterSlider):
    def update(self, attrname, old, new):
        self.data.s = self.slider.value
        self.data.update_data()
