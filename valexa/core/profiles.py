from __future__ import annotations
from enum import Enum
from typing import List, Dict, Optional, Union
import matplotlib.pyplot as plt

from scipy.stats import t

import math
import numpy as np
import pandas as pd
import mpl_toolkits.axisartist as AA
import io

from valexa.core.models import Model, ModelsManager
from valexa.core.dataobject import DataObject

class ProfileManager:

    def __init__( self, compound_name: str, data: Dict[str, pd.DataFrame], calibration_data: pd.DataFrame = None,
                  tolerance_limit: float = 80, acceptance_limit: float = 20, quantity_units: str = None,
                  rolling_data: bool = False, rolling_data_limit: int = 3, model_to_test: Union[List[str], str] = None,
                  generate_figure: bool = False) -> None:
        """
        Init ProfileManager with the necessary data
        :param compound_name: This is the name of the compounds for the profile
        :param validation_data: These are the validation data in the form of a Dataframe
        :param calibration_data: (Optional) These are the calibration data in the form of a Dataframe. If it is omitted,
        it will be assumed that the validation data are in absolute form and will only build one profile.
        :param tolerance_limit: (Optional) The tolerance limit (beta). Default = 80
        :param acceptance_limit: (Optional) The acceptance limit (lambda). Default = 20
        :param quantity_units: (Optional) The units (%, mg/l, ppm, ...) of the introduced data. This is only to
        ease the reading of the output.
        :param rolling_data: (Optional) If this is set to True, the system will do multiple iteration with the data and
        generate multiple profile with each subset of data.
        :param rolling_data_limit: (Optional) In combination with rolling_data, this is the minimum lenght of the subset
        that rolling_data will go to. Default = 3.
        :param model_to_test: (Optional) A list of model to test, if not set the system will test them all.
        :param generate_figure: (Optional) Generate a plot of the profile.
        """
        self.compound_name: str = compound_name
        self.quantity_units: str = quantity_units
        self.stats_limits: Dict[str, float] = {
            "Tolerance": tolerance_limit,
            "Acceptance": acceptance_limit
        }
        self.tolerance_limit: float = tolerance_limit
        self.acceptance_limit: float = acceptance_limit
        self.data: Dict[str, pd.DataFrame] = data
        self.rolling_data: bool = rolling_data
        if type(model_to_test)==str:
            model_to_test = [model_to_test]
        self.model_to_test: List[str] = model_to_test
        self.rolling_data_limit: int = rolling_data_limit
        self.generate_figure: bool = generate_figure

        self.model_manager: ModelsManager = ModelsManager()
        self.model_manager.initialize_models(self.model_to_test)

        self.data_objects: List[DataObject] = self.__get_dataobject
        self.profiles = None

    def make_profiles( self, models: List[str] = None) -> None:
        if type(models)==str:
            models = [models]
        list_of_models: List[str] = self.model_manager.initialized_models_list
        profiles: Dict[str, List[Profile]] = {}
        if models is None:
            if self.model_to_test is None:
                models = list_of_models
            else:
                models = self.model_to_test

        for model_name in models:
            if model_name in list_of_models:
                print(model_name)
                profiles[model_name] = self.__get_profiles(model_name)
                print("Number of profile: " + str(len(profiles[model_name])))

        self.profiles = profiles

    def __get_profiles(self, model_name: str = None) -> List[Profile]:
        profiles: List[Profile] = []
        for data_object in self.data_objects:
            if "Calibration" in self.data:
                current_profile: Profile = Profile(self.model_manager.modelize(model_name, data_object))
            else:
                current_profile: Profile = Profile(data_object)
            current_profile.calculate(self.stats_limits)
            if self.generate_figure:
                current_profile.make_plot()
            profiles.append(current_profile)

        return profiles

    @property
    def __get_dataobject( self ) -> List[DataObject]:
        validation_dict: Dict[str, pd.DataFrame] = {}
        data_to_model: List[DataObject] = []
        if "Calibration" in self.data:
            calibration_dict: Dict[str, pd.DataFrame] = {}
            if self.rolling_data:
                validation_dict = self.__sliding_window_data(self.data["Validation"])
                calibration_dict = self.__sliding_window_data(self.data["Calibration"])
            else:
                validation_dict["All"] = self.data["Validation"]
                calibration_dict["All"] = self.data["Calibration"]

            for validation_key in validation_dict.keys():
                for calibration_key in calibration_dict.keys():
                    data_to_model.append(DataObject(validation_dict[validation_key], calibration_dict[calibration_key]))

        else:
            if self.rolling_data:
                validation_dict = self.__sliding_window_data(self.data["Validation"])
            else:
                validation_dict["All"] = self.data["Validation"]

            for validation_key in validation_dict.keys():
                data_to_model.append(DataObject(validation_dict[validation_key]))

        data_to_model = self.__sanitize_data_to_model(data_to_model)

        return data_to_model

    def __sliding_window_data( self, data: pd.DataFrame ) -> Dict[str, pd.DataFrame]:
        data_level: np.ndarray = data["Level"].unique()
        data_dict: Dict[str, pd.DataFrame] = dict()
        for window_size in range(self.rolling_data_limit - 1, len(data_level) + 1):
            for window_location in range(0, len(data_level) - window_size):
                start_level: int = data_level[window_location]
                end_level: int = data_level[window_location + window_size]
                level_name: str = str(start_level) + "->" + str(end_level)
                data_dict[level_name]: pd.DataFrame = data[(data["Level"] >= start_level) & (data["Level"] <= end_level)]
                data_dict[level_name].reset_index(drop=True, inplace=True)

        return data_dict

    def __sanitize_data_to_model( self, data_to_model: List[DataObject] ) -> List[DataObject]:
        data_to_keep: List[DataObject] = []
        for data_object in data_to_model:
            if data_object.calibration_data is not None:
                if (data_object.calibration_first_concentration/2) < data_object.validation_first_concentration and data_object.calibration_last_concentration > data_object.validation_last_concentration:
                    data_to_keep.append(data_object)

        return data_to_keep


class ProfileLevel:
    def __init__( self, level_data: pd.DataFrame):
        self.data: pd.DataFrame = level_data
        self.introduced_concentration: float = None
        self.calculated_concentration: float = None
        self.bias: float = None
        self.relative_bias: float = None
        self.recovery: float = None
        self.repeatability_var: float = None
        self.repeatability_std: float = None
        self.repeatability_std_pc: float = None
        self.inter_series_var: float = None
        self.inter_series_std: float = None
        self.inter_series_std_pc: float = None
        self.intermediate_precision_std: float = None
        self.abs_tolerance: List[float] = []
        self.rel_tolerance: List[float] = []
        self.acceptance_interval: List[float] = []
        self.sum_square_error_intra_series: float = None
        self.series_by_group: Dict = {}
        self.nb_series: int = None
        self.nb_measures: int = None
        self.nb_rep: int = None
        self.fidelity_var: float = None
        self.fidelity_std: float = None
        self.ratio_var: float = None
        self.b_coefficient: float = None
        self.degree_of_freedom: float = None
        self.tolerance_std: float = None
        self.abs_uncertainty: float = None
        self.rel_uncertainty: float = None
        self.pc_uncertainty: float = None

    def calculate( self, tolerance_limit: float ):
        #self.series_by_group = self.__series_by_group()
        self.nb_series: int = self.data["Serie"].nunique()
        self.nb_measures: int = len(self.data.index)
        self.nb_rep: float = self.nb_measures / self.nb_series
        self.introduced_concentration: np.float = self.data["x"].mean()
        self.calculated_concentration: np.float = self.data["x_calc"].mean()
        self.bias = self.calculated_concentration - self.introduced_concentration
        self.relative_bias = (self.bias / self.introduced_concentration) * 100
        self.recovery = (self.calculated_concentration / self.introduced_concentration) * 100
        self.repeatability_var = self.get_repeatability_var()
        self.repeatability_std = math.sqrt(self.repeatability_var)
        self.repeatability_std_pc = self.repeatability_std / self.calculated_concentration * 100
        self.inter_series_var = self.get_inter_series_var()
        self.inter_series_std = math.sqrt(self.inter_series_var)
        self.inter_series_std_pc = self.inter_series_std / self.calculated_concentration * 100
        self.fidelity_var = np.sum([self.repeatability_var, self.inter_series_var])
        self.fidelity_std = math.sqrt(self.fidelity_var)
        self.ratio_var = self.get_ratio_var()
        self.b_coefficient = (self.ratio_var + 1) / (self.nb_rep * self.ratio_var + 1)
        self.degree_of_freedom = (self.ratio_var + 1) ** 2 / ((self.ratio_var + (1 / self.nb_rep)) ** 2 /
                                                              (self.nb_series - 1) + (
                                                                      1 - (1 / self.nb_rep)) / self.nb_measures)
        self.tolerance_std = self.fidelity_std * (math.sqrt(1 + (1 / (self.nb_measures * self.b_coefficient))))
        self.abs_tolerance = self.get_absolute_tolerance(tolerance_limit)
        self.rel_tolerance = [(tol / self.introduced_concentration) * 100 for tol in self.abs_tolerance]
        self.abs_uncertainty = self.tolerance_std * 2
        self.rel_uncertainty = self.abs_uncertainty / self.calculated_concentration
        self.pc_uncertainty = self.abs_uncertainty / self.introduced_concentration * 100

    def get_repeatability_var( self ) -> float:
        repeatability_var = 0
        sum_square_errors = 0
        for (k, series) in self.series_by_group.items():
            series_mean_result = np.mean([s.result for s in series])
            sum_square_errors += np.sum([(rep.result - series_mean_result) ** 2 for rep in series])
        self.sum_square_error_intra_series = sum_square_errors

        if sum_square_errors > 0:
            repeatability_var = sum_square_errors / (self.nb_series * (self.nb_rep - 1))
        return repeatability_var

    def get_inter_series_var( self ) -> float:
        sum_square_errors_total = np.sum(np.square(self.data['x'] - self.data['x_calc']))
        sum_square_errors_inter_series = sum_square_errors_total - self.sum_square_error_intra_series

        if sum_square_errors_inter_series <= 0:
            return 0

        inter_series_var: float = ((sum_square_errors_inter_series / (
                self.nb_series - 1)) - self.repeatability_var) / self.nb_rep
        if inter_series_var < 0:
            return 0

        return inter_series_var

    def get_ratio_var( self ) -> float:
        if self.inter_series_var == 0 or self.repeatability_var == 0:
            ratio_var = 0
        else:
            ratio_var = self.inter_series_var / self.repeatability_var

        return ratio_var

    def get_absolute_tolerance( self, tolerance_limit: int ) -> List[float]:

        student_low = t.ppf(1 - ((1 - (tolerance_limit / 100)) / 2), int(math.floor(self.degree_of_freedom)))
        student_high = t.ppf(1 - ((1 - (tolerance_limit / 100)) / 2), int(math.ceil(self.degree_of_freedom)))

        cover_factor = student_low - (student_low - student_high) * (
                self.degree_of_freedom - math.floor(self.degree_of_freedom))
        tolerance_low = self.calculated_concentration - cover_factor * self.tolerance_std
        tolerance_high = self.calculated_concentration + cover_factor * self.tolerance_std

        return [tolerance_low, tolerance_high]


class Direction(Enum):
    IN = 1
    OUT = 2


class Intersect:

    def __init__( self, value: float, direction: Direction ):
        self.value = value
        self.direction = direction


class Profile:
    LIMIT_LOWER = 0
    LIMIT_UPPER = 1

    def __init__( self, model: Union[Model, DataObject]):
        self.model = model
        self.acceptance_interval: List[float] = []
        self.min_loq: float = None
        self.max_loq: float = None
        self.lod: float = None
        self.has_limits = False
        self.image_data = None
        self.fig = None
        self.profile_levels: List[ProfileLevel] = []
        for level in self.model.list_of_levels:
            self.profile_levels.append(ProfileLevel(self.model.get_level(level)))

    def calculate( self , stats_limits: Union[Dict[str, float], None] = None):
        if stats_limits is None:
            stats_limits = {"Tolerance": 80, "Acceptance": 20}
        acceptance_limit = stats_limits["Acceptance"]
        tolerance_limit = stats_limits["Tolerance"]
        self.acceptance_interval = [(1 - (acceptance_limit / 100)) * 100, (1 + (acceptance_limit / 100)) * 100]
        for level in self.profile_levels:
            level.calculate(tolerance_limit)
        try:
            self.min_loq, self.max_loq = self.get_limits_of_quantification(acceptance_limit)
            self.lod = self.min_loq / 3.3
            self.has_limits = True
        except ValueError as e:
            self.min_loq = None
            self.max_loq = None
            self.lod = None

    def get_limits_of_quantification( self, acceptance_limit: int ) -> (float, float):

        intersects_low = []
        intersects_high = []

        for l in range(len(self.profile_levels) - 1):
            level_a = self.profile_levels[l]
            level_b = self.profile_levels[l + 1]
            lower_intersect = self.get_intersect_between_levels(level_a, level_b, acceptance_limit, self.LIMIT_LOWER)
            upper_intersect = self.get_intersect_between_levels(level_a, level_b, acceptance_limit, self.LIMIT_UPPER)
            if lower_intersect:
                intersects_low.append(lower_intersect)
            if upper_intersect:
                intersects_high.append(upper_intersect)

        lower_limits = self.get_limits_from_intersects(intersects_low, acceptance_limit, self.LIMIT_LOWER)
        upper_limits = self.get_limits_from_intersects(intersects_high, acceptance_limit, self.LIMIT_UPPER)

        limits = self.get_most_restrictive_limits(lower_limits, upper_limits)

        return limits

    def get_intersect_between_levels( self, level_a, level_b, accept_limit: int, limit_type ) -> Intersect:
        level_a_tol = level_a.abs_tolerance[limit_type]
        level_b_tol = level_b.abs_tolerance[limit_type]
        if limit_type == self.LIMIT_LOWER:
            lambda_accept = 1 - (accept_limit / 100)
        elif limit_type == self.LIMIT_UPPER:
            lambda_accept = 1 + (accept_limit / 100)
        else:
            raise ValueError("Limit type not valid. Valid options are: Profile.LOWER_LIMIT or Profile.UPPER_LIMIT")

        level_a_accept_limit = level_a.introduced_concentration * lambda_accept
        level_b_accept_limit = level_b.introduced_concentration * lambda_accept

        tol_slope = (level_b_tol - level_a_tol) / (
                level_b.introduced_concentration - level_a.introduced_concentration)
        tol_origin = level_a_tol - tol_slope * level_a.introduced_concentration

        accept_slope = (level_b_accept_limit - level_a_accept_limit) / (
                level_b.introduced_concentration - level_a.introduced_concentration)
        accept_origin = level_a_accept_limit - accept_slope * level_a.introduced_concentration

        value = (accept_origin - tol_origin) / (tol_slope - accept_slope)
        if value > level_b.introduced_concentration or value < level_a.introduced_concentration:
            return None

        if level_a_tol >= level_a_accept_limit and level_b_tol < level_b_accept_limit:
            if limit_type == self.LIMIT_LOWER:
                direction = Direction.OUT
            else:
                direction = Direction.IN
        elif level_a_tol < level_a_accept_limit and level_b_tol >= level_b_accept_limit:
            if limit_type == self.LIMIT_LOWER:
                direction = Direction.IN
            else:
                direction = Direction.OUT
        else:
            raise ValueError("Cannot identify intersect's direction")

        return Intersect(value, direction)

    def get_limits_from_intersects( self, intersects: List[Intersect], accept_limit: int, limit_type: int ) -> (
            float, float):

        if len(intersects) == 0:
            low_accept_limit_rel = (1 - (accept_limit / 100)) * 100
            high_accept_limit_rel = (1 + (accept_limit / 100)) * 100
            mean_tolerance = np.mean([l.rel_tolerance[limit_type] for l in self.profile_levels])
            if low_accept_limit_rel <= mean_tolerance <= high_accept_limit_rel:
                limits = (self.profile_levels[0].introduced_concentration, self.profile_levels[-1].introduced_concentration)
            else:
                raise ValueError("Not valid limit of quantification detected")
        elif len(intersects) == 1 and intersects[0].direction == Direction.IN:
            limits = (intersects[0].value, self.profile_levels[-1].introduced_concentration)
        elif len(intersects) == 1 and intersects[0].direction == Direction.OUT:
            limits = (self.profile_levels[0].introduced_concentration, intersects[0].value)
        elif len(intersects) == 2:
            if intersects[0].direction == Direction.IN and intersects[1].direction == Direction.OUT:
                limits = (intersects[0].value, intersects[1].value)
            elif intersects[0].direction == Direction.OUT and intersects[1].direction == Direction.IN:
                limits = (intersects[1].value, self.profile_levels[-1].introduced_concentration)
            else:
                raise ValueError("Intersects pair not valid: possible values (IN, OUT) or (OUT, IN)")
        elif len(intersects) > 2:
            in_out_pairs = self.group_intersects_by_in_out(intersects)
            if len(in_out_pairs) == 1:
                min_limit = in_out_pairs[0][0].value
                max_limit = in_out_pairs[0][1].value
                limits = (min_limit, max_limit)
            elif len(in_out_pairs) > 1:
                min_limit = in_out_pairs[-1][0].value
                max_limit = in_out_pairs[-1][1].value
                limits = (min_limit, max_limit)
        else:
            raise ValueError("Cannot define limits from intersects")

        return limits

    def group_intersects_by_in_out( self, intersects: List[Intersect] ) -> List:
        in_out_pairs = []
        current_in_intersect = None
        for i in intersects:
            if i.direction == Direction.IN:
                current_in_intersect = i
            elif current_in_intersect and i.direction == Direction.OUT:
                in_out_pairs.append((current_in_intersect, i))
                current_in_intersect = None
        return in_out_pairs

    def get_most_restrictive_limits( self, lower_limits, upper_limits ) -> (float, float):
        min_limit = max(lower_limits[0], upper_limits[0])
        max_limit = min(lower_limits[1], upper_limits[1])

        return min_limit, max_limit

    def make_plot( self ):

        fig = plt.figure()
        ax = AA.Subplot(fig, 111)
        fig.add_subplot(ax)

        levels_x = np.array([l.introduced_concentration for l in self.profile_levels])
        y_recovery = np.array([l.recovery for l in self.profile_levels])
        y_error = np.array([s.pc_uncertainty for s in self.profile_levels])
        ax.axis["bottom", "top", "right"].set_visible(False)
        ax.axis["y=100"] = ax.new_floating_axis(nth_coord=0, value=100)
        ax.plot(levels_x, [l.rel_tolerance[0] for l in self.profile_levels], linewidth=1.0, color="b",
                label="Min tolerance limit")
        ax.plot(levels_x, [l.rel_tolerance[1] for l in self.profile_levels], linewidth=1.0, color="g",
                label="Max tolerance limit")
        ax.plot(levels_x, [self.acceptance_interval[0] for _ in self.profile_levels], "k--", label="Acceptance limit")
        ax.plot(levels_x, [self.acceptance_interval[1] for _ in self.profile_levels], "k--")
        results_x = [s.introduced_concentration for s in self.profile_levels]
        results_y = [(s.calculated_concentration / s.introduced_concentration) * 100 for s in self.profile_levels]
        ax.scatter(results_x, results_y, alpha=0.5, s=2)
        ax.errorbar(levels_x, y_recovery, yerr=y_error, color="m", linewidth=2.0, marker=".", label="Recovery")
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Recovery (%)")
        ax.legend(loc=1)

        self.fig = fig

        self.image_data = io.BytesIO()
