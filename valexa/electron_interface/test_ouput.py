import pandas as pd
from valexa.profiles import ProfileManager

def test_ouptut(data):
    data = format_json_dict(data)

    aa = ProfileManager(
        "Test",
        data,
        model_to_test=["Linear"]
    )

    aa.make_profiles()

    print(aa.output_profiles("json"))

def format_json_dict(data):
    data_formatted = {}

    data_formatted["Validation"] = pd.DataFrame(data["Validation"])
    data_formatted["Calibration"] = pd.DataFrame(data["Calibration"])

    return data_formatted