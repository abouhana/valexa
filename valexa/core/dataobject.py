import pandas as pd

from typing import Dict, Union, List

class DataObject:

    def __init__( self, validation_data: pd.DataFrame, validation_levels: str, calibration_data: pd.DataFrame = None,
                  calibration_levels: str = None ):
        self._validation_data: pd.DataFrame = validation_data
        self._validation_levels: str = validation_levels
        self._calibration_data: Union[pd.DataFrame, None] = calibration_data
        self._calibration_levels: Union[str, None] = calibration_levels

    def add_calculated_value( self, calculated_value: pd.DataFrame) -> None:
        self._validation_data = pd.concat([self._validation_data, calculated_value], axis=1)

    @property
    def validation_data( self ) -> pd.DataFrame:
        return self._validation_data

    @property
    def calibration_data( self ) -> Union[pd.DataFrame, None]:
        return self._calibration_data

    @property
    def validation_levels( self ) -> str:
        return self._validation_levels

    @property
    def calibration_levels( self ) -> Union[str, None]:
        return self._calibration_levels

    @property 
    def data_x( self ) -> pd.DataFrame:
        return self._validation_data["x"]

    @property
    def data_y( self ) -> pd.DataFrame:
        if self._calibration_data is None:
            return self._validation_data["y"]
        else:
            return self._validation_data["x_calc"]