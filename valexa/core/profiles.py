from collections import defaultdict
from operator import attrgetter
from typing import List, Dict

from scipy.stats import t

import math
import numpy as np

from valexa.core.standard import Standard
from valexa.core.models import Result, ModelHandler, Model

DEFAULT_TOLERANCE = 80
DEFAULT_ACCEPTANCE = 20


def make_profiles(calib_data: List[tuple], valid_data: List[tuple], tolerance_limit: int,
                  acceptance_limit: int) -> List:
    std_calib = Standard(calib_data)
    std_valid = Standard(valid_data)
    model_handler = ModelHandler(std_calib, std_valid)

    models = model_handler.get_models()

    profiles = []
    for model in models:
        profile = Profile(model)
        profile.calculate(tolerance_limit, acceptance_limit)
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
        self.acceptance_interval: List[float] = []

    def add_result(self, result):
        self.series.append(result)

    def calculate(self, tolerance_limit: int = DEFAULT_TOLERANCE):
        self.introduced_concentration = np.mean([s.concentration for s in self.series])
        self.calculated_concentration = np.mean([s.result for s in self.series])
        self.bias = self.calculated_concentration - self.introduced_concentration
        self.relative_bias = (self.bias / self.introduced_concentration)*100
        self.recovery = (self.calculated_concentration / self.introduced_concentration) * 100
        self.repeatability_var = self.get_repeatability_var()
        self.repeatability_std = np.sqrt(self.repeatability_var)
        self.inter_series_var = self.get_inter_series_var()
        self.inter_series_std = np.sqrt(self.inter_series_var)
        self.absolute_tolerance = self.get_absolute_tolerance(tolerance_limit)
        self.relative_tolerance = [(tol / self.introduced_concentration) * 100 for tol in self.absolute_tolerance]

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

    def get_absolute_tolerance(self, tolerance_limit: int) -> List[float]:
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
        student_low = t.ppf(1 - (tolerance_limit / 100), math.floor(degree_of_freedom))
        student_high = t.ppf(1 - (tolerance_limit / 100), math.ceil(degree_of_freedom))

        cover_factor = student_low - (student_low - student_high) * (degree_of_freedom - math.floor(degree_of_freedom))
        tolerance_std = fidelity_std * np.sqrt(1 + 1 / (nb_measure * b_coefficient))
        tolerance_low = self.calculated_concentration - tolerance_std * cover_factor
        tolerance_high = self.calculated_concentration + tolerance_std * cover_factor

        return [tolerance_low, tolerance_high]

    def __series_by_group(self) -> Dict:
        series_group = defaultdict(list)
        for s in self.series:
            series_group[s.series].append(s)

        return series_group


class Profile:
    def __init__(self, model: Model):
        self.model = model
        self.series = model.series_calculated
        self.levels: List[ProfileLevel] = []
        self.acceptance_interval: List[float] = []

        self.__split_series_by_levels()
        self.levels.sort(key=attrgetter('index'))

    def __split_series_by_levels(self):
        for s in self.series:
            try:
                level = [level for level in self.levels if level.index == s.level][0]
                level.add_result(s)
            except IndexError:
                level = ProfileLevel(index=s.level)
                level.add_result(s)
                self.levels.append(level)

    def calculate(self, tolerance_limit: int = DEFAULT_TOLERANCE, acceptance_limit: int = DEFAULT_ACCEPTANCE):
        self.acceptance_interval = [(1-(acceptance_limit/100))*100, (1+(acceptance_limit/100))*100]
        for level in self.levels:
            level.calculate(tolerance_limit)

    def make_plot(self, ax):
        levels_x = [l.calculated_concentration for l in self.levels]
        ax.axis["bottom", "top", "right"].set_visible(False)
        ax.axis["y=100"] = ax.new_floating_axis(nth_coord=0, value=100)
        ax.plot(levels_x, [l.recovery for l in self.levels], color="m", linewidth=2.0, marker=".", label="Recovery")
        ax.plot(levels_x, [l.relative_tolerance[0] for l in self.levels], linewidth=1.0, color="b", label="Max tolerance limit")
        ax.plot(levels_x, [l.relative_tolerance[1] for l in self.levels], linewidth=1.0, color="g", label= "Min tolerance limit")
        ax.plot(levels_x, [self.acceptance_interval[0] for _ in self.levels], "k--", label="Acceptance limit")
        ax.plot(levels_x, [self.acceptance_interval[1] for _ in self.levels], "k--")
        results_x = [s.concentration for s in self.series]
        results_y = [(s.result/s.concentration)*100 for s in self.series]
        ax.scatter(results_x, results_y, alpha=0.5, s=2)
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Recovery (%)")
        ax.legend(loc=1)
