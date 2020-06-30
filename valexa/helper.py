import sigfig as sf
import pandas as pd

def get_value_between(
        x_value: float, left_coord: (float, float), right_coord: (float, float)
) -> float:
    x1, y1 = left_coord
    x2, y2 = right_coord
    slope: float = (y2 - y1) / (x2 - x1)

    return slope * (x_value - x1) + y1

def format_json_to_dict(data):
    return {
        "Validation": pd.DataFrame(data["Validation"]),
        "Calibration": pd.DataFrame(data["Calibration"])
    }

def round(data, sigfig):
    if type(data).__module__ == "numpy":
        return sf.round(data.item(), sigfig)
    else:
        return sf.round(data, sigfig)

