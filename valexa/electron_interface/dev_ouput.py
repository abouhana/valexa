import pandas as pd
from valexa.profiles import ProfileManager
import json

def dev_ouptut(data):
    data = format_json_dict(data)

    aa = ProfileManager(
        "Test",
        data,
        model_to_test=["Linear"]
    )

    aa.make_profiles()

    bb = aa.output_profiles()
    oo = {"type": "PROFILE", "data": bb}
    print(json.dumps(oo))

def format_json_dict(data):
    data_formatted = {}

    data_formatted["Validation"] = pd.DataFrame(data["Validation"])
    data_formatted["Calibration"] = pd.DataFrame(data["Calibration"])

    return data_formatted