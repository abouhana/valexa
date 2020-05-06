import pandas as pd
import numpy as np

from typing import Union, Optional


class DataObject:

    def __init__(self, validation_data: pd.DataFrame, calibration_data: pd.DataFrame = None):
        self.validation_data: pd.DataFrame = validation_data
        self.validation_first_level: int = min(self.validation_data["Level"].unique())
        self.validation_last_level: int = max(self.validation_data["Level"].unique())
        self.validation_levels: int = self.validation_data["Level"].nunique()
        self.validation_first_concentration: float = min(self.validation_data["x"])
        self.validation_last_concentration: float = max(self.validation_data["x"])

        self.calibration_data: Optional[pd.DataFrame] = calibration_data
        if self.calibration_data is not None:
            self.calibration_first_level: int = min(self.calibration_data["Level"].unique())
            self.calibration_last_level: int = max(self.calibration_data["Level"].unique())
            self.calibration_levels: int = self.calibration_data["Level"].nunique()
            self.calibration_first_concentration: float = min(self.calibration_data["x"])
            self.calibration_last_concentration: float = max(self.calibration_data["x"])

    def add_calculated_value(self, calculated_value: pd.DataFrame) -> None:
        self.validation_data = pd.concat([self.validation_data, calculated_value], axis=1)

    def get_level(self, level) -> Optional[pd.DataFrame]:
        return self.validation_data[self.validation_data["Level"] == level]

    @property
    def data_x_calc(self) -> Optional[pd.Series]:
        if "x_calc" in self.validation_data:
            return self.validation_data["x_calc"]
        else:
            return None

    @property
    def data_x(self) -> pd.Series:
        return self.validation_data["x"]


    @property
    def data_y(self) -> pd.Series:
        return self.validation_data["y"]

    @property
    def list_of_series(self) -> np.ndarray:
        return self.validation_data["Serie"].unique()

    @property
    def list_of_levels(self) -> np.ndarray:
        return self.validation_data["Level"].unique()
