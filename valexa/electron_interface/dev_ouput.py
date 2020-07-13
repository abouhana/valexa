import pandas as pd
from valexa.profiles import ProfileManager
import json
import valexa.helper as vx


def dev_ouptut(data, config=""):
    data = vx.format_json_to_data(data)

    config = {
        "compound_name": "test",
        "model_to_test": "Linear",
        "rolling_data": False
    }

    aa = ProfileManager(
        "Test", data, model_to_test=["Linear"], rolling_data=False
    )

    aa.make_profiles()

    bb = aa.output_profiles()
    print(json.dumps({"type": "PROFILE", "data": "START"}))
    for zz in bb.values():
        print(json.dumps({"type": "PROFILE", "data": zz}))
    print(json.dumps({"type": "PROFILE", "data": "STOP"}))
