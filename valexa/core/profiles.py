from collections import defaultdict
from typing import List, Dict
from scipy.stats import t

import math
import numpy as np

from valexa.core.standard import Standard, Result


def make_profiles(calib_data: List[tuple], valid_data: List[tuple]) -> List:
    std_calib = Standard(calib_data)
    std_valid = Standard(valid_data)

    models_parameters = std_calib.get_models_parameters()
    models_results = std_valid.apply_models(models_parameters)

    profiles = []
    for results in models_results:
        profile = Profile(results)
        profile.calculate()
        profiles.append(profile)

    return profiles


class ProfileLevel:
    def __init__(self, index):
        self.index = index
        self.series: List[Result] = []
        self.introduced_concentration: float = None
        self.calculated_concentration: float = None
        self.bias: float = None
        self.relative_bias: float = None
        self.recovery: float = None
        self.repeatability_var: float = None
        self.repeatability_std: float = None
        self.inter_series_var: float = None
        self.inter_series_std: float = None
        self.intermediate_precision_std: float = None
        self.absolute_tolerance: List[float] = []
        self.relative_tolerance: List[float] = []

    def add_result(self, result):
        self.series.append(result)

    def calculate(self):
        self.introduced_concentration = np.mean([s.concentration for s in self.series])
        self.calculated_concentration = np.mean([s.result for s in self.series])
        self.bias = self.calculated_concentration - self.introduced_concentration
        self.relative_bias = self.bias / self.introduced_concentration
        self.recovery = (self.calculated_concentration / self.introduced_concentration) * 100
        self.repeatability_var = self.get_repeatability_var()
        self.repeatability_std = np.sqrt(self.repeatability_var)
        self.inter_series_var = self.get_inter_series_var()
        self.inter_series_std = np.sqrt(self.inter_series_var)
        self.absolute_tolerance = self.get_absolute_tolerance()
        self.relative_tolerance = [(t/self.introduced_concentration)*100 for t in self.absolute_tolerance]

    def get_repeatability_var(self) -> float:
        repeatability_var = 0
        sum_square_errors = 0
        series_group = self.__series_by_group()
        for (k, series) in series_group.items():
            series_mean_result = np.mean([s.result for s in series_group[k]])
            for rep in series:
                sum_square_errors += (rep.result - series_mean_result) ** 2

        if sum_square_errors > 0:
            repeatability_var = sum_square_errors / (len(self.series) - len(series_group.keys()))
        return repeatability_var

    def get_inter_series_var(self) -> float:
        sum_square_errors = 0
        series_group = self.__series_by_group()
        nb_rep = len(self.series) / len(series_group.keys())
        for (k, series) in series_group.items():
            series_mean_result = np.mean([s.result for s in series_group[k]])
            sum_square_errors += (series_mean_result - self.calculated_concentration) ** 2

        if sum_square_errors > 0:
            inter_series_var = ((sum_square_errors / (len(series_group.keys()) - 1)) -
                                self.repeatability_var) / nb_rep
            if inter_series_var < 0:
                return 0
            else:
                return inter_series_var

    def get_absolute_tolerance(self) -> List[float]:
        fidelity_var = np.sum([self.repeatability_var, self.inter_series_var])
        fidelity_std = np.sqrt(fidelity_var)
        if self.inter_series_var == 0 or self.repeatability_var == 0:
            variance_report = 0
        else:
            variance_report = self.inter_series_var / self.repeatability_var

        series_group = self.__series_by_group()
        nb_series = len(series_group.keys())
        nb_measure = len(self.series)
        nb_rep = nb_measure / nb_series

        b_coefficient = (variance_report + 1) / (nb_rep * variance_report + 1)
        degree_of_freedom = (variance_report + 1) ** 2 / (
                (variance_report + 1 / nb_rep) ** 2 / (nb_series - 1) + (1 - 1 / nb_rep) / nb_measure)
        student_interval = t.interval(0.80, round(degree_of_freedom))

        cover_factor = student_interval[0] - (student_interval[0] - student_interval[1]) * (
                    degree_of_freedom - math.floor(degree_of_freedom))
        tolerance_std = fidelity_std*np.sqrt(1+1/(nb_measure*b_coefficient))
        tolerance_low = self.calculated_concentration-tolerance_std*cover_factor
        tolerance_high = self.calculated_concentration+tolerance_std*cover_factor

        return [tolerance_low, tolerance_high]

    def __series_by_group(self) -> Dict:
        series_group = defaultdict(list)
        for s in self.series:
            series_group[s.series].append(s)

        return series_group


class Profile:
    def __init__(self, model_results: List[Result]):
        self.levels: List[ProfileLevel] = []

        self.__split_series_by_levels(model_results)

    def __split_series_by_levels(self, series):
        for s in series:
            try:
                level = [level for level in self.levels if level.index == s.level][0]
                level.add_result(s)
            except IndexError:
                level = ProfileLevel(index=s.level)
                level.add_result(s)
                self.levels.append(level)

    def calculate(self):
        for level in self.levels:
            level.calculate()
