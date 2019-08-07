from collections import namedtuple, defaultdict
from typing import List, DefaultDict

Entry = namedtuple('Entry', ['series', 'level', 'concentration', 'response'])


class Standard:
    def __init__(self, data: List[tuple]):
        self.series: DefaultDict[List[Entry]] = defaultdict(list)

        self.__handle_data(data)

    def __handle_data(self, data: List[tuple]):
        for d in data:
            entry: Entry = Entry._make(d)
            self.series[entry.series].append(entry)
