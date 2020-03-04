from typing import List, Tuple, Any, Optional, Hashable

import numpy as np
from collections import namedtuple

import pandas as pd
import statsmodels.formula.api as smf
from pandas import Series
from sympy import solve, Symbol
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication, parse_expr
from patsy import dmatrix


from valexa.core.standard import Standard, Entry
from valexa.core.models_list import model_list

Result = namedtuple('Result', ['series', 'level', 'concentration', 'result'])




class Model:

    def __init__(self, model_info) :
        self.series_params = {}
        self.series_calculated: list = []
        self.has_correction: bool = False
        self.correction_factor: float = None
        self.full_fit_info = {}
        self.name: str = model_info["name"]
        self.formula: str = model_info["formula"]
        if model_info["weight"] is None:
            self.weight: str = "I(x/x) - 1"
        else:
            self.weight: str = "I(" + model_info["weight"] + ") - 1"

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
            model = Model(model_list(degree))
            model.degree = degree
            print("Starting model: " + model.name)
            for (key, entries) in self.calib_std.series.items():
                model.range = [min([e.concentration for e in entries]), max([e.concentration for e in entries])]
                fitted_model = self.__get_model_fit(model, entries)
                model.full_fit_info[key] = fitted_model
                model.series_params[key] = fitted_model.params
                model.series_calculated.extend(self.__apply_params_to_series(key, model))
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
            func_to_solve = self.__build_function_from_params(function_params)
            x = Symbol("x")
            root_value = solve(func_to_solve, x)
            if len(root_value)>0:
                result_value = min(root_value)
            else:
                result_value = 0
            result = Result(entry.series, entry.level, entry.concentration, result_value)
            results.append(result)

        return results

    def __build_function_from_params(self, params: pd.DataFrame):
        function_string: str = ""
        for param in params.iteritems():
            if param[0] == "Intercept":
                function_string += "-" + str(param[1])
            elif param[0].startswith("I("):
                if param[0][2:3] == "y":
                    function_string += "-" + str(param[1])
                else:
                    function_string += "+" + str(param[1]) + "*" + param[0][2:-1]
            else:
                if param[0][0:1] == "y":
                    function_string += "-" + str(param[1])
                else:
                    function_string += "+" + str(param[1]) + "*" + param[0]

        func = parse_expr(function_string)
        return func
