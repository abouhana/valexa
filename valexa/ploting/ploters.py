import json
from typing import Dict, List

from valexa.core.profiles import (DEFAULT_ACCEPTANCE, DEFAULT_TOLERANCE,
    Profile, make_profiles)
from valexa.core.xlsx import XlsxHandler
from valexa.ploting.plotly.canvas import ProfilePlotCanvas


class PloterData:

    handler = XlsxHandler
    profiles = []
    tolerance_limit = DEFAULT_TOLERANCE
    acceptance_limit = DEFAULT_ACCEPTANCE

    def __init__(self, file: str or File, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError("%s() received an invalid keyword %r. Only "
                                "arguments that are already attributes of the "
                                "class are accepted." % (self.__name__, key))
            else:
                setattr(self, key, value)

        self.load_data(file)

    def load_data(self, file: str or File) -> None:
        handler = self.handler(file)

        self.profiles = make_profiles(
            handler.get_calibration_data(), 
            handler.get_validation_data(), 
            self.tolerance_limit, 
            self.acceptance_limit
        )
