from typing import Callable, Dict, Union, OrderedDict
from valexa.core.profiles import ProfileManager

import pandas as pd

class Optimizer:

    def __init__(self, profile_manager: ProfileManager, optimizer_parameters: OrderedDict[str, Union[str, bool]]):

        self.parameter_function: Dict[str, Callable] = {
            "has_limits": self.__get_has_limits,
            "min_loq": self.__get_min_loq,
            "model.fit.rsquared": self.__get_model_fit_rsquared,
            "max_loq": self.__get_max_loq,
            "lod": self.__get_lod,
            "model.data.calibration_levels": self.__get_model_data_calibration_levels
        }

        self.profile_manager = profile_manager
        self.parameters = optimizer_parameters

        self.profile_value = self.get_profile_value()
        self.sorted_profile = self.sort_profile()

    def sort_profile( self ) -> pd.DataFrame:
        boolean_parameter: OrderedDict[str, bool] = {}
        ascending_parameter: OrderedDict[str, bool] = {}
        final_dataframe: pd.DataFrame = self.profile_value
        for key, value in self.parameters.items():
            if type(value)==bool:
                boolean_parameter[key] = value

        for key, value in self.parameters.items():
            if value=="max":
                ascending_parameter[key] = False
            elif value=="min":
                ascending_parameter[key] = True

        for parameter in boolean_parameter:
            final_dataframe = final_dataframe[final_dataframe[parameter]==self.parameters[parameter]]

        final_dataframe = final_dataframe.sort_values(by=list(ascending_parameter.keys()), ascending=ascending_parameter.values())

        return final_dataframe

    def get_profile_value( self ) -> pd.DataFrame:
        results: pd.DataFrame = pd.DataFrame()
        for parameter in self.parameters.keys():
            if len(results)==0:
                results =  self.parameter_function[parameter]()
            else:
                results = pd.merge(results,  self.parameter_function[parameter](), on=["Model", "Index"])

        return results

    def __get_model_fit_rsquared( self ) -> pd.DataFrame:
        return self.__get_profile_model_fit("rsquared")

    def __get_model_data_calibration_levels( self ) -> pd.DataFrame:
        return self.__get_profile_model_data("calibration_levels")

    def __get_min_loq( self ) -> pd.DataFrame:
        return self.__get_profile_value("min_loq")

    def __get_max_loq( self ) -> pd.DataFrame:
        return self.__get_profile_value("max_loq")

    def __get_lod( self ) -> pd.DataFrame:
        return self.__get_profile_value("lod")

    def __get_has_limits( self ) -> pd.DataFrame:
        return self.__get_profile_value("has_limits")


    def __get_profile_value( self, parameter ) -> pd.DataFrame:
        return_value: pd.DataFrame = pd.DataFrame()
        for profile_type in self.profile_manager.profiles.keys():
            for key, profile in enumerate(self.profile_manager.profiles[profile_type]):
                temp_dataframe = pd.DataFrame([[profile_type, key, getattr(profile, parameter)]],
                                              columns=["Model", "Index", parameter])
                return_value = return_value.append(temp_dataframe, ignore_index=True)
        return return_value

    def __get_profile_model_fit( self, parameter ) -> pd.DataFrame:
        return_value: pd.DataFrame = pd.DataFrame()
        for profile_type in self.profile_manager.profiles.keys():
            for key, profile in enumerate(self.profile_manager.profiles[profile_type]):
                temp_dataframe = pd.DataFrame([[profile_type, key, getattr(profile.model.fit, parameter)]],
                                              columns=["Model", "Index", "model.fit." + parameter])
                return_value = return_value.append(temp_dataframe, ignore_index=True)
        return return_value

    def __get_profile_model_data( self, parameter ) -> pd.DataFrame:
        return_value: pd.DataFrame = pd.DataFrame()
        for profile_type in self.profile_manager.profiles.keys():
            for key, profile in enumerate(self.profile_manager.profiles[profile_type]):
                temp_dataframe = pd.DataFrame([[profile_type, key, getattr(profile.model.data, parameter)]],
                                              columns=["Model", "Index", "model.data." + parameter])
                return_value = return_value.append(temp_dataframe, ignore_index=True)
        return return_value

    @property
    def available_parameters( self ):
        return self.parameter_function.keys()