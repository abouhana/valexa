from typing import List, Tuple, Any

import numpy as np
from collections import namedtuple

import pandas as pd
import statsmodels.formula.api as smf
from sympy import solve, Symbol
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr
from patsy import dmatrix


from valexa.core.standard import Standard, Entry

Result = namedtuple('Result', ['series', 'level', 'concentration', 'result'])


class Model:

    def __init__(self, name: str = "Linear", formula: str = "Linear", weight: str = None):
        self.degree: int = None
        self.series_params = {}
        self.series_calculated: pd.DataFrame =
        self.has_correction: bool = False
        self.correction_factor: float = None
        self.full_fit_info = {}
        self.name: str = name
        self.formula: str = formula
        if weight is None:
            self.weight: str = "I(x/x) - 1"
        else:
            self.weight: str = "I(" + weight + ") - 1"

    # @property
    # def function(self):
    #     try:
    #         return self.EQUATION_BY_DEGREE[self.degree]["function"]
    #     except KeyError:
    #         return lambda p, x: p["x"] * x + p["Intercept"] - p["y"]

    def handle_correction(self):
        recoveries = [(s.result / s.concentration) * 100 for s in self.series_calculated]
        recovery_avg = np.mean(recoveries)

        if abs(100 - recovery_avg) >= 4:
            self.has_correction = True
            self.correction_factor = round(1 / (recovery_avg / 100), 2)
            self.__apply_correction()

    def __apply_correction(self):
        corrected_results = []
        for s in self.series_calculated:
            value_corrected = s.result * self.correction_factor
            corrected_results.append(s._replace(result=value_corrected))

        self.series_calculated = corrected_results


class ModelHandler:
    DEFAULT_MAX_DEGREE = 11

    def __init__(self, calib_std: Standard, valid_std: Standard):
        self.calib_std = calib_std
        self.valid_std = valid_std

    def get_models(self, max_degree: int = DEFAULT_MAX_DEGREE) -> List[Model]:
        models = []
        for degree in range(1, max_degree + 1):
            model = Model()
            model.degree = degree
            print("Starting model: " + model.name)
            for (key, entries) in self.calib_std.series.items():
                model.range = [min([e.concentration for e in entries]), max([e.concentration for e in entries])]
                fitted_model = self.__get_model_fit(model, entries)
                model.series_params[key] = fitted_model.params
                model.series_calculated.extend(self.__apply_params_to_series(key, model))
                model.full_fit_info[key] = fitted_model
            model.handle_correction()
            models.append(model)
            print(model.name + " done")
        return models

    def __get_model_fit(self, model: Model, entries: List[Entry]):
        x_value: List[Any] = [e.concentration for e in entries]
        y_value: List[Any] = [e.response for e in entries]
        df = pd.DataFrame({'x':x_value, 'y':y_value})
        fitted_model = smf.wls(formula=model.formula, weights=dmatrix(model.weight, df), data=df).fit()
        return fitted_model

    def __get_y_err(self, entries: List[Entry]) -> List:
        y_error = []
        for lvl in np.unique([e.level for e in entries]):
            y_error.append(np.std([e.response for e in entries if e.level == lvl]))
        return y_error

    def __apply_params_to_series(self, index: int, model: Model) -> List[Result]:
        results = []
        for entry in self.valid_std.series[index]:
            function_params = model.series_params[index]
            function_params["y"] = entry.response
            transformations = (standard_transformations + (implicit_multiplication_application,))
            root_value = solve(model.function(function_params, x), x)
            if len(root_value)>0:
                result_value = min(root_value)
            else:
                result_value = 0
            result = Result(entry.series, entry.level, entry.concentration, result_value)
            results.append(result)

        return results
