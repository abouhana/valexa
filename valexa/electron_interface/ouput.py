import pandas as pd
from valexa.profiles import ProfileManager
import json
import valexa.helper as vx


def ouptut(**config):
    print(json.dumps({"type": "PROFILE", "data": "START"}))
    config['data'] = vx.format_json_to_data(config['data'])

    profiles = ProfileManager(**config)

    profiles.make_profiles()

    profiles = profiles.output_profiles()
    for profile in profiles.values():
        print(json.dumps({"type": "PROFILE", "data": profile}).replace(": NaN", ': "null"'))
    print(json.dumps({"type": "PROFILE", "data": "STOP"}))
