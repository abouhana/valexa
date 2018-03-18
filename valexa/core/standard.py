from collections import namedtuple, defaultdict
from typing import List, Dict, DefaultDict

import numpy as np

Entry = namedtuple('Entry', ['series', 'level', 'concentration', 'response'])
Result = namedtuple('Result', ['series', 'level', 'concentration', 'result'])

ModelsParameters = List[Dict]
ModelsResults = List[Dict]


class Standard:
    def __init__(self, data: List[tuple]):
        self.series: DefaultDict[List[Entry]] = defaultdict(list)

        self.__handle_data(data)

    def __handle_data(self, data: List[tuple]):
        for d in data:
            entry: Entry = Entry._make(d)
            self.series[entry.series].append(entry)

    def get_models_parameters(self, max_degree=3) -> ModelsParameters:
        models_parameters: ModelsParameters = []
        for degree in range(max_degree):
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
            series_results = {}
            for (key, params) in model.items():
                results = []
                for s in self.series[key]:
                    p_func = np.poly1d(params)
                    result = Result(s.series, s.level, s.concentration, p_func(s.response))
                    print(result)
                    results.append(result)
                series_results[key] = results
            models_results.append(series_results)

        return models_results


