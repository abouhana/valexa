from typing import List

import numpy as np
from collections import namedtuple

from valexa.core.standard import Standard

Result = namedtuple('Result', ['series', 'level', 'concentration', 'result'])


class Model:
    NAME_BY_DEGREE = {
        1: "Linear",
        2: "Quadratic"
    }

    def __init__(self):
        self.degree: int = None
        self.series_params = {}
        self.series_calculated: List[Result] = []

    @property
    def name(self) -> str:
        try:
            return self.NAME_BY_DEGREE[self.degree]
        except KeyError:
            return "Unknown model"


class ModelHandler:
    DEFAULT_MAX_DEGREE = 2

    def __init__(self, calib_std: Standard, valid_std: Standard):
        self.calib_std = calib_std
        self.valid_std = valid_std

    def get_models(self, max_degree: int = DEFAULT_MAX_DEGREE) -> List[Model]:
        models = []
        for degree in range(1, max_degree + 1):
            model = Model()
            model.degree = degree
            for (key, entries) in self.calib_std.series.items():
                x_value = [e.concentration for e in entries]
                y_value = [e.response for e in entries]
                parameters = np.polyfit(x_value, y_value, degree)
                model.series_params[key] = parameters
                model.series_calculated.extend(self.__apply_params_to_series(key, parameters))
            models.append(model)
        return models

    def __apply_params_to_series(self, index: int, parameters) -> List[Result]:
        results = []
        for entry in self.valid_std.series[index]:
            p_func = np.poly1d(parameters)
            result_value = (p_func - entry.response).roots[-1]
            result = Result(entry.series, entry.level, entry.concentration, result_value)
            results.append(result)

        return results
