import pandas as pd
from typing import Dict, Optional, Union, List

TestDataSet = Dict[str, Dict[str, pd.DataFrame]]


def dataset( data_set_name: Optional[str] = None ) -> Union[List[str], Dict[str, pd.DataFrame]]:
    """
    These are example dataset that can be used to help you understand or test the library.
    The format of a dataset should be a dict with at least a Validation dataset and optionally a Calibration dataset.
    Both dataset should be pandas DataFrame with the following columns: Serie, Level, x, y.
    The Calibration dataset can have either one serie or a number of serie equal to the Validation dataset. If there is
    only one Calibration serie, Valexa will assume that the same calibration is used for all Validation series, else it
    will use a different calibration for each series.
    In the case of a dataset with no Calibration dataset, the Y dataset will be considered to be absolute (such as bacterial
    count for example).
    The source of the dataset found in this example are as follow:
    inra_pyrene: Huyez-Levrat, M et al.,Cahier technique de l'INRA - Validation des méthodes (2010), https://www6.inrae.fr/cahier_des_techniques/Les-Cahiers-parus/Les-n-Speciaux-et-les-n-Thematiques/Validation-des-methodes
    feinberg_nicotinamide: Feinberg, M., Labo-Stat (2010), https://www.lavoisier.fr/livre/sciences-de-la-vie/labo-stat/feinberg/descriptif-9782743014261
    inter_test: Own dataset (HPLC-UV) (2020)
    feinberg_coli: Feinberg, M. et al., Validation of Alternative Methods for the Analysis of Drinking Water and Their Application to Escherichia coli (2011), https://dx.doi.org/10.1128/AEM.00020-11
    :param data_set_name: Name of the dataset to return
    :return: A dict of DataFram
    """
    dataset_data: TestDataSet = {
        "inra_pyrene": {
            "Validation": pd.DataFrame([
                [1, 1, 1.9, 36539],
                [1, 1, 1.9, 36785],
                [2, 1, 1.9, 60086],
                [2, 1, 1.9, 35295],
                [3, 1, 1.9, 57695],
                [3, 1, 1.9, 59731],
                [1, 2, 4.7, 102066],
                [1, 2, 4.7, 98495],
                [2, 2, 4.7, 99897],
                [2, 2, 4.7, 93547],
                [3, 2, 4.7, 115298],
                [3, 2, 4.7, 111584],
                [1, 3, 9.5, 188665],
                [1, 3, 9.5, 191294],
                [2, 3, 9.5, 188657],
                [2, 3, 9.5, 198683],
                [3, 3, 9.5, 221678],
                [3, 3, 9.5, 194983],
                [1, 4, 28.5, 595999],
                [1, 4, 28.5, 604704],
                [2, 4, 28.5, 520857],
                [2, 4, 28.5, 501025],
                [3, 4, 28.5, 557258],
                [3, 4, 28.5, 541355]
            ], columns=["Serie", "Level", "x", "y"]),
            "Calibration": pd.DataFrame([
                [1, 1, 0.9, 43083],
                [2, 1, 0.9, 24719],
                [3, 1, 0.9, 35684],
                [1, 2, 4.6, 117767],
                [2, 2, 4.6, 112319],
                [3, 2, 4.6, 115840],
                [1, 3, 9.2, 238120],
                [2, 3, 9.2, 202957],
                [3, 3, 9.2, 249807],
                [1, 4, 18.4, 450132],
                [2, 4, 18.4, 398342],
                [3, 4, 18.4, 440029],
                [1, 5, 27.6, 682393],
                [2, 5, 27.6, 611523],
                [3, 5, 27.6, 633748]
            ], columns=["Serie", "Level", "x", "y"])
        },
        "feinberg_nicotinamide": {
            "Validation": pd.DataFrame([
                [1, 1, 0.4, 22.6],
                [1, 1, 0.4, 22.1],
                [1, 1, 0.4, 22.4],
                [2, 1, 0.4, 23.3],
                [2, 1, 0.4, 24.1],
                [2, 1, 0.4, 23.9],
                [3, 1, 0.4, 23.8],
                [3, 1, 0.4, 23.6],
                [3, 1, 0.4, 23.5],
                [1, 2, 2, 135],
                [1, 2, 2, 135.1],
                [1, 2, 2, 129.9],
                [2, 2, 2, 137.6],
                [2, 2, 2, 135.2],
                [2, 2, 2, 138.8],
                [3, 2, 2, 136.3],
                [3, 2, 2, 135.1],
                [3, 2, 2, 134.4],
                [1, 3, 4, 275.2],
                [1, 3, 4, 276.9],
                [1, 3, 4, 261.3],
                [2, 3, 4, 268.1],
                [2, 3, 4, 269.7],
                [2, 3, 4, 276.9],
                [3, 3, 4, 271.6],
                [3, 3, 4, 273.3],
                [3, 3, 4, 275]
            ], columns=["Serie", "Level", "x", "y"]),
            "Calibration": pd.DataFrame([
                [1, 1, 0.4, 22.7],
                [1, 1, 0.4, 23.1],
                [2, 1, 0.4, 22.9],
                [2, 1, 0.4, 23.2],
                [3, 1, 0.4, 21.9],
                [3, 1, 0.4, 22.1],
                [1, 2, 4, 281.6],
                [1, 2, 4, 275.3],
                [2, 2, 4, 275.3],
                [2, 2, 4, 274.6],
                [3, 2, 4, 272.0],
                [3, 2, 4, 273.0]
            ], columns=["Serie", "Level", "x", "y"])
        },
        "intern_test": {
            "Calibration": pd.DataFrame([
                [1, 1, 0.98, 5],
                [1, 2, 3.9, 13],
                [1, 3, 15.635, 58],
                [1, 4, 62.5, 230],
                [1, 5, 250, 890],
                [1, 6, 500, 1616],
                [1, 7, 1000, 3310],
                [1, 1, 0.98, 5],
                [1, 2, 3.9, 19],
                [1, 3, 15.635, 57],
                [1, 4, 62.5, 219],
                [1, 5, 250, 898],
                [1, 6, 500, 1623],
                [1, 7, 1000, 3294],
                [1, 1, 0.98, 6],
                [1, 2, 3.9, 16],
                [1, 3, 15.635, 63],
                [1, 4, 62.5, 230],
                [1, 5, 250, 887],
                [1, 6, 500, 1660],
                [1, 7, 1000, 3298]
            ], columns=["Serie", "Level", "x", "y"]),
            "Validation": pd.DataFrame([
                [1, 1, 0.7765, 6],
                [1, 2, 1.563, 8],
                [1, 3, 6.25, 25],
                [1, 4, 25, 93],
                [1, 5, 100, 348],
                [1, 1, 0.7765, 7],
                [1, 2, 1.563, 12],
                [1, 3, 6.25, 25],
                [1, 4, 25, 96],
                [1, 5, 100, 350],
                [1, 1, 0.7765, 9],
                [1, 2, 1.563, 13],
                [1, 3, 6.25, 27],
                [1, 4, 25, 89],
                [1, 5, 100, 349],
                [2, 1, 0.7765, 5],
                [2, 2, 1.563, 11],
                [2, 3, 6.25, 28],
                [2, 4, 25, 91],
                [2, 5, 100, 332],
                [2, 1, 0.7765, 5],
                [2, 2, 1.563, 11],
                [2, 3, 6.25, 31],
                [2, 4, 25, 92],
                [2, 5, 100, 329],
                [2, 1, 0.7765, 6],
                [2, 2, 1.563, 13],
                [2, 3, 6.25, 26],
                [2, 4, 25, 90],
                [2, 5, 100, 333],
                [2, 1, 0.7765, 3],
                [2, 2, 1.563, 8],
                [2, 3, 6.25, 25],
                [2, 4, 25, 94],
                [2, 5, 100, 333],
                [2, 1, 0.7765, 4],
                [2, 2, 1.563, 12],
                [2, 3, 6.25, 32],
                [2, 4, 25, 98],
                [2, 5, 100, 351],
                [2, 1, 0.7765, 9],
                [2, 2, 1.563, 10],
                [2, 3, 6.25, 34],
                [2, 4, 25, 97],
                [2, 5, 100, 345],
                [3, 1, 0.7765, 7],
                [3, 2, 1.563, 6],
                [3, 3, 6.25, 24],
                [3, 4, 25, 98],
                [3, 5, 100, 370],
                [3, 1, 0.7765, 6],
                [3, 2, 1.563, 9],
                [3, 3, 6.25, 27],
                [3, 4, 25, 95],
                [3, 5, 100, 361],
                [3, 1, 0.7765, 6],
                [3, 2, 1.563, 12],
                [3, 3, 6.25, 21],
                [3, 4, 25, 101],
                [3, 5, 100, 364]
            ], columns=["Serie", "Level", "x", "y"])
        },
        "feinberg_coli": {
            "Validation": pd.DataFrame([
                [1, 1, 5, 9],
                [1, 1, 10, 10],
                [2, 1, 19, 18],
                [2, 1, 10, 14],
                [3, 1, 10, 14],
                [3, 1, 8, 11],
                [4, 1, 14, 10],
                [4, 1, 12, 14],
                [5, 1, 14, 15],
                [5, 1, 11, 11],
                [6, 1, 9, 8],
                [6, 1, 6, 3],
                [7, 1, 9, 12],
                [7, 1, 13, 9],
                [8, 1, 4, 15],
                [8, 1, 11, 7],
                [9, 1, 9, 18],
                [9, 1, 12, 11],
                [10, 1, 13, 9],
                [10, 1, 9, 8],
                [11, 1, 15, 9],
                [11, 1, 8, 12],
                [1, 2, 39, 53],
                [1, 2, 29, 36],
                [2, 2, 72, 62],
                [2, 2, 52, 53],
                [3, 2, 65, 95],
                [3, 2, 64, 78],
                [4, 2, 67, 48],
                [4, 2, 66, 78],
                [5, 2, 52, 34],
                [5, 2, 56, 38],
                [6, 2, 30, 62],
                [6, 2, 50, 89],
                [7, 2, 55, 56],
                [7, 2, 51, 59],
                [8, 2, 33, 88],
                [8, 2, 44, 50],
                [9, 2, 53, 66],
                [9, 2, 54, 62],
                [10, 2, 46, 59],
                [10, 2, 65, 74],
                [11, 2, 45, 59],
                [11, 2, 52, 48],
                [1, 3, 105, 202],
                [1, 3, 112, 130],
                [2, 3, 139, 145],
                [2, 3, 142, 118],
                [3, 3, 105, 201],
                [3, 3, 124, 145],
                [4, 3, 146, 200],
                [4, 3, 124, 200],
                [5, 3, 80, 50],
                [5, 3, 78, 50],
                [6, 3, 70, 130],
                [6, 3, 90, 130],
                [7, 3, 131, 145],
                [7, 3, 136, 130],
                [8, 3, 89, 130],
                [8, 3, 90, 200],
                [9, 3, 130, 118],
                [9, 3, 133, 202],
                [10, 3, 130, 202],
                [10, 3, 112, 130],
                [11, 3, 90, 118],
                [11, 3, 74, 165]
            ], columns=["Serie", "Level", "x", "y"])
        }
    }

    if data_set_name is None:
        return list(dataset_data.keys())
    else:
        try:
            return dataset_data[data_set_name]
        except KeyError:
            print("Invalid dataset name, the available name are: " + ", ".join(list(dataset_data.keys())))
            raise