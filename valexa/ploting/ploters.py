import json
from typing import Dict, List

from valexa.core.profiles import (DEFAULT_ACCEPTANCE, DEFAULT_TOLERANCE,
    Profile, make_profiles)
from valexa.core.xlsx import XlsxHandler
from valexa.ploting.plotly.canvas import ProfilePlotCanvas


class PloterData:

    handler = XlsxHandler
    calib_data = None
    valid_data = None
    profiles = []
    tolerance_limit = DEFAULT_TOLERANCE
    acceptance_limit = DEFAULT_ACCEPTANCE

    def __init__(self, file: str or File=None, **kwargs):
        if file:
            self.load_data(file)

        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError("%s() received an invalid keyword %r. Only "
                                "arguments that are already attributes of the "
                                "class are accepted." % (self.__name__, key))
            else:
                setattr(self, key, value)

    def load_data(self, file: str or File) -> None:
        handler = self.handler(file)
        self.calib_data = handler.get_calibration_data()
        self.valid_data = handler.get_validation_data()

        self.profiles = make_profiles(
            self.calib_data, self.valid_data, 
            self.tolerance_limit, self.acceptance_limit
        )

    def reset(self):
        self.__init__()