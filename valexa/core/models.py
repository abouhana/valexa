from __future__ import annotations

import pandas as pd
import numpy as np
import copy
import statsmodels.formula.api as smf
import statsmodels.regression.linear_model as sm
from sympy import lambdify, solveset, S
from sympy.abc import x
from patsy.highlevel import dmatrix

from warnings import warn
from typing import List, Dict, Union, Callable, Optional

from valexa.core.models_list import model_list
from valexa.core.dataobject import DataObject

ModelInfo = Dict[str, Optional[str]]


class ModelsManager:

    def __init__(self, models_source: str = "hardcoded"):
        self.available_models: Dict[str, Dict[str, str]] = self.get_available_models(models_source)
        self.models: Dict[str, ModelGenerator] = {}

    def initialize_models(self, models_name: List = None) -> ModelsManager:
        if models_name is not None:
            for model in models_name:
                if self.get_model_info(model) is not None:
                    self.models[model] = ModelGenerator(model, self.get_model_info(model))
        else:
            for model in self.available_models:
                self.models[model] = ModelGenerator(model, self.get_model_info(model))

        if len(self.models) == 0:
            warn("No model to initialize")

        return self

    def modelize( self, model_name: str, model_data: DataObject ) -> Model:
        return self.models[model_name].calculate_model(model_data)

    def get_available_models( self, models_source: str = "hardcoded" ) -> Dict[str, Dict[str, str]]:
        # This will eventually handle model through SQL or other database
        list_of_models:  Union[Model, Dict[str, ModelInfo]] = {}

        if models_source == "hardcoded":
            list_of_models = model_list()

        return list_of_models

    def get_model_weight( self, model_name: str ) -> Optional[str]:
        if model_name in self.available_models:
            return self.available_models[model_name]["weight"]
        else:
            warn("Model name not found, returning None")
            return None

    def get_model_formula( self, model_name: str ) -> Optional[str]:
        if model_name in self.available_models:
            return self.available_models[model_name]["formula"]
        else:
            warn("Model name not found, returning None")
            return None

    def get_model_info( self, model_name: str ) -> Optional[Dict[str, str]]:
        if model_name in self.available_models:
            return self.available_models[model_name]
        else:
            warn("Model name not found, returning None")
            return None

    @property
    def number_of_models( self ) -> int:
        return len(list(self.available_models.keys()))

    @property
    def initialized_models_list( self ) -> List[str]:
        return list(self.available_models.keys())

class Model:

    def __init__( self, data: DataObject, model_formula: str, model_weight: str):

        self.data: DataObject = copy.deepcopy(data)
        self.formula: str = model_formula
        self.weight: str = model_weight
        self.fit: sm.RegressionResultsWrapper = self.__get_model_fit
        self.root_function: Callable = self.__build_function_from_params
        self.data.add_calculated_value(self.__get_model_roots)

    @property
    def __get_model_fit( self ) -> sm.RegressionResultsWrapper:
        return smf.wls(formula=self.formula, weights=dmatrix(self.weight, self.data.calibration_data),
                       data=self.data.calibration_data).fit()

    @property
    def __get_model_roots( self ) -> pd.DataFrame:
        list_of_roots: List[Union[float, None]] = []
        for validation_value in self.data.validation_data.iterrows():
            root_value: pd.DataFrame = pd.DataFrame(
                solveset(self.root_function(x)-validation_value[1]["y"], x, S.Reals).evalf())
            if len(root_value) > 0:
                list_of_roots.append(root_value[0][0])
            else:
                list_of_roots.append(None)
        return pd.DataFrame(list_of_roots, columns=["x_calc"])

    @property
    def __build_function_from_params( self ) -> Callable:
        function_string: str = ""
        for param, value in self.fit.params.items():
            if param == "Intercept":
                function_string += "-" + str(value)
            elif param.startswith("I("):
                function_string += "+" + str(value) + "*" + param[2:-1]
            else:
                function_string += "+" + str(value) + "*" + param

        return lambdify(x, function_string)

    def get_level( self, level ) -> Union[pd.DataFrame, None]:
        return self.data.get_level(level)

    @property
    def data_x( self ) -> pd.Series:
        return self.data.data_x

    @property
    def data_y( self ) -> pd.Series:
        return self.data.data_y

    @property
    def list_of_series( self ) -> np.ndarray:
        return self.data.list_of_series

    @property
    def list_of_levels( self ) -> np.ndarray:
        return self.data.list_of_levels

    @property
    def validation_data( self ) -> pd.DataFrame:
        return self.data.validation_data

    @property
    def calibration_data( self ) -> pd.DataFrame:
        return self.data.calibration_data

class ModelGenerator:

    def __init__( self, model_name: str, model_info: Dict[str, str] ):

        self.name: str = model_name
        self.formula: str = model_info["formula"]
        if model_info["weight"] is None:
            self.weight: str = "I(x/x) - 1"
        else:
            self.weight: str = "I(" + model_info["weight"] + ") - 1"

    def calculate_model( self, data: DataObject ) -> Model:
        return Model(data, self.formula, self.weight)