from __future__ import annotations

import pandas as pd
import numpy as np
import copy
import statsmodels.formula.api as smf
import statsmodels.regression.linear_model as sm
from sympy import lambdify, solveset, S
from sympy.abc import x
from sympy.sets.sets import EmptySet
from patsy.highlevel import dmatrix

from warnings import warn
from typing import List, Dict, Union, Callable, Optional

from valexa.models_list import model_list
from valexa.dataobject import DataObject

ModelInfo = Dict[str, Optional[str]]
FitInfo = Union[sm.RegressionResultsWrapper, Dict[int, sm.RegressionResultsWrapper]]


class ModelsManager:
    def __init__(self, models_source: str = "hardcoded"):
        self.available_models: Dict[str, Dict[str, str]] = self.get_available_models(
            models_source
        )
        self.models: Dict[str, ModelGenerator] = {}

    def initialize_models(self, models_name: Union[List, str] = None) -> ModelsManager:
        if models_name is not None:

            if type(models_name) == str:
                models_name = [models_name]

            for model in models_name:
                if self.get_model_info(model) is not None:
                    self.models[model] = ModelGenerator(
                        model, self.get_model_info(model)
                    )
        else:
            for model in self.available_models:
                self.models[model] = ModelGenerator(model, self.get_model_info(model))

        if len(self.models) == 0:
            warn("No model initialized")

        return self

    def modelize(self, model_name: str, model_data: DataObject) -> Model:
        return self.models[model_name].calculate_model(model_data)

    @staticmethod
    def get_available_models(
        models_source: str = "hardcoded",
    ) -> Dict[str, Dict[str, str]]:
        # This will eventually handle model through SQL or other database
        list_of_models: Union[Model, Dict[str, ModelInfo]] = {}

        if models_source == "hardcoded":
            list_of_models = model_list()

        return list_of_models

    def get_model_weight(self, model_name: str) -> Optional[str]:
        if model_name in self.available_models:
            return self.available_models[model_name]["weight"]
        else:
            warn("Model name not found, try get_available_models() for a list of available models")
            return None

    def get_model_formula(self, model_name: str) -> Optional[str]:
        if model_name in self.available_models:
            return self.available_models[model_name]["formula"]
        else:
            warn("Model name not found, try get_available_models() for a list of available models")
            return None

    def get_model_info(self, model_name: str) -> Optional[Dict[str, str]]:
        if model_name in self.available_models:
            return self.available_models[model_name]
        else:
            warn("Model name not found, try get_available_models() for a list of available models")
            return None

    @property
    def number_of_models(self) -> int:
        return len(list(self.available_models.keys()))

    @property
    def initialized_models_list(self) -> List[str]:
        return list(self.models.keys())


class Model:
    def __init__(
        self, data: DataObject, model_formula: str, model_weight: str, model_name: str
    ):

        self.data: DataObject = copy.deepcopy(data)
        self.name = model_name
        self.formula: str = model_formula
        self.weight: str = model_weight
        if len(self.list_of_series("validation")) == len(
            self.list_of_series("calibration")
        ):
            self.multiple_calibration: bool = True
            temp_fit: Dict[int, sm.RegressionResultsWrapper] = {}
            temp_root_function: Dict[int, Callable] = {}
            for serie in self.list_of_series("calibration"):
                temp_fit[serie] = self.__get_model_fit(serie)
                temp_root_function[serie]: Dict[
                    int, Callable
                ] = self.__build_function_from_params(temp_fit, serie)
        else:
            self.multiple_calibration: bool = False
            temp_fit: sm.RegressionResultsWrapper = self.__get_model_fit()
            temp_root_function: Callable = self.__build_function_from_params(temp_fit)

        self.fit: FitInfo = temp_fit
        self.root_function: Union[Callable, Dict[int, Callable]] = temp_root_function
        self.data.add_calculated_value(self.__get_model_roots)
        self.rsquared: Optional[float] = None
        if self.multiple_calibration:
            self.rsquared = np.mean([s.rsquared for s in self.fit.values()])
        else:
            self.rsquared = self.fit.rsquared

    def __get_model_fit(
        self, serie: Optional[int] = None
    ) -> sm.RegressionResultsWrapper:
        if serie is None:
            calibration_data: pd.DataFrame = self.data.calibration_data
        else:
            calibration_data: pd.DataFrame = self.data.get_serie(serie, "calibration")
        return smf.wls(
            formula=self.formula,
            weights=dmatrix(self.weight, calibration_data),
            data=calibration_data,
        ).fit()

    def __sanitize_roots( self, root_set ):
        if type(root_set) != EmptySet:
            return pd.DataFrame(root_set.evalf())
        else:
            return pd.DataFrame()

    @property
    def __get_model_roots(self) -> pd.Series:
        list_of_roots: List[Union[float, None]] = []
        for validation_value in self.data.validation_data.iterrows():
            root_value: pd.DataFrame = pd.DataFrame()
            if self.multiple_calibration:
                root_value = self.__sanitize_roots(
                        solveset(
                            self.root_function[validation_value[1]["Serie"]](x)
                            - validation_value[1]["y"],
                            x,
                            S.Reals
                        )
                    )
            else:
                root_value = self.__sanitize_roots(
                        solveset(
                            self.root_function(x) - validation_value[1]["y"], x, S.Reals
                        )
                    )

            if len(root_value) > 0:
                list_of_roots.append(float(root_value[0][0]))
            else:
                list_of_roots.append(None)
        return pd.Series(list_of_roots)

    @staticmethod
    def __build_function_from_params(
        fitted_function: FitInfo, serie: Optional[int] = None
    ) -> Callable:
        function_string: str = ""
        if serie is None:
            params_items = fitted_function.params.items()
        else:
            params_items = fitted_function[serie].params.items()
        for param, value in params_items:
            if param == "Intercept":
                function_string += "+" + str(value)
            elif param.startswith("I("):
                function_string += "+" + str(value) + "*" + param[2:-1]
            else:
                function_string += "+" + str(value) + "*" + param

        return lambdify(x, function_string)

    def get_level(
        self, level: int, serie_type: str = "validation"
    ) -> Optional[pd.DataFrame]:
        return self.data.get_level(level, serie_type)

    def get_serie(
        self, serie: int, serie_type: str = "validation"
    ) -> Optional[pd.DataFrame]:
        return self.data.get_serie(serie, serie_type)

    @property
    def data_x_calc(self) -> Optional[pd.Series]:
        return self.data.data_x_calc

    def data_x(self, serie_type: str = "validation") -> Optional[pd.Series]:
        return self.data.data_x(serie_type)

    def data_y(self, serie_type: str = "validation") -> Optional[pd.Series]:
        return self.data.data_y(serie_type)

    def list_of_series(self, serie_type: str = "validation") -> Optional[np.ndarray]:
        return self.data.list_of_series(serie_type)

    def list_of_levels(self, serie_type: str = "validation") -> Optional[np.ndarray]:
        return self.data.list_of_levels(serie_type)

    @property
    def validation_data(self) -> pd.DataFrame:
        return self.data.validation_data

    @property
    def calibration_data(self) -> pd.DataFrame:
        return self.data.calibration_data


class ModelGenerator:
    def __init__(self, model_name: str, model_info: Dict[str, str]):

        self.name: str = model_name
        self.formula: str = model_info["formula"]
        if model_info["weight"] is None:
            self.weight: str = "I(x/x) - 1"
        else:
            self.weight: str = "I(" + model_info["weight"] + ") - 1"

    def calculate_model(self, data: DataObject) -> Model:
        return Model(data, self.formula, self.weight, self.name)
