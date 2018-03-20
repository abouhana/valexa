from collections import namedtuple, defaultdict
from typing import List, Dict, DefaultDict

import numpy as np

Entry = namedtuple('Entry', ['series', 'level', 'concentration', 'response'])
Result = namedtuple('Result', ['series', 'level', 'concentration', 'result'])

ModelsParameters = List[Dict]
ModelsResults = List[List[Result]]


class Standard:
    def __init__(self, data: List[tuple]):
        self.series: DefaultDict[List[Entry]] = defaultdict(list)

        self.__handle_data(data)

    def __handle_data(self, data: List[tuple]):
        for d in data:
            entry: Entry = Entry._make(d)
            self.series[entry.series].append(entry)

    def get_models_parameters(self, max_degree=2) -> ModelsParameters:
        models_parameters: ModelsParameters = []
        for degree in range(1, max_degree + 1):
            series_parameters = {}
            for (key, s) in self.series.items():
                x_value = [e.concentration for e in s]
                y_value = [e.response for e in s]
                parameters = np.polyfit(x_value, y_value, degree)
                series_parameters[key] = parameters
            models_parameters.append(series_parameters)

        return models_parameters

    def apply_models(self, parameters: ModelsParameters) -> ModelsResults:
        models_results: ModelsResults = []
        for model in parameters:
            results = []
            for (key, params) in model.items():
                for s in self.series[key]:
                    p_func = np.poly1d(params)
                    result_value = (p_func - s.response).roots[-1]
                    result = Result(s.series, s.level, s.concentration, result_value)
                    results.append(result)
            models_results.append(results)

        return models_results
