from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Optional

from bokeh.models import FuncTickFormatter, Select
from bokeh.models import Slider, CustomJS
from data import Data


# Base class
class ParameterSlider(ABC):
    def __init__(self, data: Data, start: float, end: float, value: float, step: float, title: str):
        self.data = data
        self.slider = Slider(start=start, end=end, value=value, step=step, title=title)
        self.slider.on_change('value', self.update)

    @abstractmethod
    def update(self, attrname: str, old: float, new: float) -> None:
        pass


# Frequency class
class FrequencySlider(ParameterSlider):
    def __init__(self, data: Data, start: float, end: float, value: float, step: float, title: str):
        super().__init__(data, start, end, value, step, title)
        self.slider.width = 1800
        self.select = None

    def add_select(self, select: ParameterSelectNyquist) -> None:
        self.select = select

    def update(self, attrname: str, old: float, new: float) -> None:
        self.data.f = self.slider.value
        self.data.update_data()
        if self.select is not None:
            self.select.update_by_slider()


# Samples class
class SamplesSlider(ParameterSlider):
    def __init__(self, data: Data, start: float, end: float, value: float, step: float, title: str):
        super().__init__(data, start, end, value, step, title)
        self.time_slider: Optional[TimeSlider] = None

    def update(self, attrname: str, old: float, new: float) -> None:
        self.data.N = int(self.slider.value)
        self.data.s = self.data.N * self.data.T  # Modify s based on the new N
        self.data.update_data()
        if self.time_slider is not None:
            self.time_slider.slider.value = self.data.s

    def add_time_slider(self, time_slider: TimeSlider) -> None:
        self.time_slider = time_slider


# Time class
class TimeSlider(ParameterSlider):
    def __init__(self, data: Data, start: float, end: float, value: float, step: float, title: str,
                 samples_slider: SamplesSlider):
        super().__init__(data, start, end, value, step, title)
        self.samples_slider = samples_slider

    def update(self, attrname: str, old: float, new: float) -> None:
        self.data.s = self.slider.value
        self.data.N = int(self.data.s / self.data.T)  # Modify N based on the new s
        if self.samples_slider is not None:
            self.samples_slider.slider.value = self.data.N
        self.data.update_data()


# Sampling frequency class
class SamplingFrequencySlider(ParameterSlider):

    def __init__(self, data: Data, start: float, end: float, value: float, step: float, title: str,
                 samples_slider: SamplesSlider):
        super().__init__(data, start, end, value, step, title)
        self.select = None
        self.samples_slider = samples_slider

    def add_select(self, select: ParameterSelectNyquist) -> None:
        self.select = select

    def update(self, attrname: str, old: float, new: float) -> None:
        self.data.fs = self.slider.value
        self.data.T = 1.0 / self.data.fs  # Modify T based on the new fs
        self.data.N = int(self.data.s / self.data.T)  # Modify N based on the new T
        self.data.update_data()
        if self.samples_slider is not None:
            self.samples_slider.slider.value = self.data.N
        if self.select is not None:
            self.select.update_by_slider()


class ParameterSelectNyquist:
    def __init__(self, data: Data, frequency_slider: FrequencySlider):
        self.frequency_slider = frequency_slider
        self.data = data
        self.select = Select(title="Option:", value="",
                             options=["", "DC", "1/4 Nyquist", "1/2 Nyquist", "Nyquist", "2 Nyquist"])
        self.select.on_change('value', self.update)

    def update_by_slider(self) -> None:
        f = self.data.f
        if f == 0:
            self.select.value = "DC"
        elif f == self.data.fs / 8:
            self.select.value = "1/4 Nyquist"
        elif f == self.data.fs / 4:
            self.select.value = "1/2 Nyquist"
        elif f == self.data.fs / 2:
            self.select.value = "Nyquist"
        elif f == self.data.fs:
            self.select.value = "2 Nyquist"
        else:
            self.select.value = ""

    def update(self, attrname: str, old: float, new: float) -> None:
        if old == new:
            return
        f = 0
        if new == "DC":
            f = 0
        elif new == "1/4 Nyquist":
            f = self.data.fs / 8
        elif new == "1/2 Nyquist":
            f = self.data.fs / 4
        elif new == "Nyquist":
            f = self.data.fs / 2
        elif new == "2 Nyquist":
            f = self.data.fs
        if new != "" and self.frequency_slider is not None:
            self.frequency_slider.slider.value = f
