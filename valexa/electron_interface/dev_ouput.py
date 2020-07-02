import pandas as pd
from valexa.profiles import ProfileManager
import json
import valexa.helper as vx


def dev_ouptut(data):
    data = vx.format_json_to_dict(data)

    aa = ProfileManager(
        "Test", data, model_to_test=["Linear", "Quadratic"], rolling_data=False
    )

    aa.make_profiles()

    bb = aa.output_profiles()
    oo = {"type": "PROFILE", "data": bb}
    print(json.dumps(oo))
