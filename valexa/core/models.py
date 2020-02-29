from typing import List, Tuple, Any

import numpy as np
from collections import namedtuple

import pandas as pd
import statsmodels.formula.api as smf
from sympy import solve, Symbol


from valexa.core.standard import Standard, Entry

Result = namedtuple('Result', ['series', 'level', 'concentration', 'result'])


class Model:

    EQUATION_BY_DEGREE = {
        1: {
            "name": "Linear",
            "formula": "y ~ x",
            "weight": lambda x, y: np.ones(len(x)),
            "function": lambda p, x: p["x"] * x + p["Intercept"] - p["y"]
        },
        2: {
            "name": "Linear though 0",
            "formula": "y ~ x - 1",
            "weight": lambda x, y: np.ones(len(x)),
            "function": lambda p, x: p["x"] * x - p["y"]
        },
        3: {
            "name": "Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": lambda x, y: np.ones(len(x)),
            "function": lambda p, x: p["I(x ** 2)"] * x**2 + p["x"] * x + p["Intercept"] - p["y"]
        },
        4: {
            "name": "1/X Weighted Linear",
            "formula": "y ~ x",
            "weight": lambda x, y: 1/np.array(x),
            "function": lambda p, x: p["x"] * x + p["Intercept"] - p["y"]
        },
        5: {
            "name": "1/X^2 Weighted Linear",
            "formula": "y ~ x",
            "weight": lambda x, y: 1/np.array(x)**2,
            "function": lambda p, x: p["x"] * x + p["Intercept"] - p["y"]
        },
        6: {
            "name": "1/Y Weighted Linear",
            "formula": "y ~ x",
            "weight": lambda x, y: 1 / np.array(y),
            "function": lambda p, x: p["x"] * x + p["Intercept"] - p["y"]
        },
        7: {
            "name": "1/Y^2 Weighted Linear",
            "formula": "y ~ x",
            "weight": lambda x, y: 1 / np.array(y)**2,
            "function": lambda p, x: p["x"] * x + p["Intercept"] - p["y"]
        },
        8: {
            "name": "1/X Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": lambda x, y: 1/np.array(x),
            "function": lambda p, x: p["I(x ** 2)"] * x**2 + p["x"] * x + p["Intercept"] - p["y"]
        },
        9: {
            "name": "1/X^2 Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": lambda x, y: 1/np.array(x)**2,
            "function": lambda p, x: p["I(x ** 2)"] * x**2 + p["x"] * x + p["Intercept"] - p["y"]
        },
        10: {
            "name": "1/Y Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": lambda x, y: 1 / np.array(y),
            "function": lambda p, x: p["I(x ** 2)"] * x**2 + p["x"] * x + p["Intercept"] - p["y"]
        },
        11: {
            "name": "1/Y^2 Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": lambda x, y: 1 / np.array(y)**2,
            "function": lambda p, x: p["I(x ** 2)"] * x**2 + p["x"] * x + p["Intercept"] - p["y"]
        }
    }

    def __init__(self):
        self.degree: int = None
        self.series_params = {}
        self.series_calculated: List[Result] = []
        self.has_correction: bool = False
        self.correction_factor: float = None
        self.full_fit_info = {}

    @property
    def name(self) -> str:
        try:
            return self.EQUATION_BY_DEGREE[self.degree]["name"]
        except KeyError:
            return "Linear"

    @property
    def formula(self) -> str:
        try:
            return self.EQUATION_BY_DEGREE[self.degree]["formula"]
        except KeyError:
            return "y ~ x"

    @property
    def weight(self):
        try:
            return self.EQUATION_BY_DEGREE[self.degree]["weight"]
        except KeyError:
            return lambda x, y: np.ones(len(x))

    @property
    def function(self):
        try:
            return self.EQUATION_BY_DEGREE[self.degree]["function"]
        except KeyError:
            return lambda p, x: p["x"] * x + p["Intercept"] - p["y"]

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
        fitted_model = smf.wls(formula=model.formula, weights=model.weight(x_value, y_value), data=df).fit()
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
            x = Symbol('x', real=True)
            root_value = solve(model.function(function_params, x), x)
            if len(root_value)>0:
                result_value = min(root_value)
            else:
                result_value = 0
            result = Result(entry.series, entry.level, entry.concentration, result_value)
            results.append(result)

        return results
