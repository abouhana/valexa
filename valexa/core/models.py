from __future__ import annotations
from warnings import warn
from typing import List, Dict, Union, Callable, Optional

import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.regression.linear_model as sm
from sympy import lambdify, solveset, S
from sympy.abc import x
from patsy import dmatrix

from valexa.core.models_list import model_list


class ModelsManager:

    def __init__(self, models_source: str = "hardcoded"):
        self.available_models: Dict[str, Dict[str, str]] = self.get_available_models(models_source)
        self.models: Dict[str, ModelGenerator] = {}

    def initialize_models(self, models_name: List = None) -> ModelsManager:
        if models_name is not None:
            for model in models_name:
                if self.get_model_info(model) is not None:
                    self.models["model"] = ModelGenerator(model, self.get_model_info(model))
        else:
            for model in self.available_models:
                self.models["model"] = ModelGenerator(model, self.get_model_info(model))

        if len(self.models) == 0:
            warn("No model to initialize")

        return self

    def get_available_models(self, models_source: str = "hardcoded") -> Dict[str, Dict[str, str]]:
        # This will eventually handle model through SQL or other database
        list_of_models: Dict[str, Dict[str, str]] = {}

        if models_source == "hardcoded":
            list_of_models = model_list()
        else:
            list_of_models = {"Linear": {"formula": "y ~ x", "weight": None}}

        return list_of_models

    def get_model_weight(self, model_name: str) -> Optional[str]:
        if model_name in self.available_models:
            return self.available_models["model_name"]["weight"]
        else:
            warn("Model name not found, returning None")
            return None

    def get_model_formula(self, model_name: str) -> Optional[str]:
        if model_name in self.available_models:
            return self.available_models["model_name"]["formula"]
        else:
            warn("Model name not found, returning None")
            return None

    def get_model_info(self, model_name: str) -> Optional[Dict[str, str]]:
        if model_name in self.available_models:
            return self.available_models["model_name"]
        else:
            warn("Model name not found, returning None")
            return None

    @property
    def number_of_models(self) -> int:
        return len(list(self.available_models.keys()))

    @property
    def initialized_models_list(self) -> List[str]:
        return list(self.available_models.keys())


class ModelGenerator:

    def __init__(self, model_name: str, model_info: Dict[str, str]):

        self.name: str = model_name
        self.formula: str = model_info["formula"]
        if model_info["weight"] is None:
            self.weight: str = "I(x/x) - 1"
        else:
            self.weight: str = "I(" + model_info["weight"] + ") - 1"

    def calculate_model(self, data) -> Model:
        return Model(data, self.formula, self.weight)


class Model:

    def __init__(self, data: Dict[str, pd.DataFrame], model_formula: str, model_weight: str):

        self.data_calibration: pd.DataFrame = data["Calibration"][["x", "y"]]
        self.data_validation: pd.DataFrame = data["Validation"][["x", "y"]]
        self.formula: str = model_formula
        self.weight: str = model_weight
        self.fit: sm.RegressionResultsWrapper = self.__get_model_fit
        self.root_function: Callable = self.__build_function_from_params
        self.roots: pd.DataFrame = self.__get_model_roots

    @property
    def __get_model_fit(self) -> sm.RegressionResultsWrapper:
        return smf.wls(formula=self.formula, weights=dmatrix(self.weight, self.data_calibration),
                       data=self.data_calibration).fit()

    @property
    def __get_model_roots(self) -> pd.DataFrame:
        list_of_roots: List[Union[float, None]] = []
        for validation_value in self.data_validation.to_list():
            root_value: pd.DataFrame = pd.DataFrame(
                solveset(self.root_function(x, validation_value[1]), x, S.Reals).evalf())
            if len(root_value) > 0:
                list_of_roots.append((root_value - validation_value[0]).abs().sort_values([0]).values[0][0])
            else:
                list_of_roots.append(None)
        return pd.DataFrame(list_of_roots, columns=["x_measured"])

    @property
    def __build_function_from_params(self) -> Callable:
        function_string: str = ""
        for param in self.fit.params.iteritems():
            if param[0] == "Intercept":
                function_string += "-" + str(param[1])
            elif param[0].startswith("I("):
                function_string += "+" + str(param[1]) + "*" + param[0][2:-1]
            else:
                function_string += "+" + str(param[1]) + "*" + param[0]

        return lambdify(x, function_string)

    @property
    def model_data(self) -> pd.DataFrame:
        return pd.concat([self.data_calibration.rename(columns={"x": "x_calibration", "y": "y_calibration"}),
                          self.data_validation.rename(columns={"x": "x_validation", "y": "y_validation"}),
                          self.roots], axis=1)

    @property
    def model_fit(self) -> sm.RegressionResultsWrapper:
        return self.model_fit

    @property
    def model_function(self) -> Callable:
        return self.model_function
