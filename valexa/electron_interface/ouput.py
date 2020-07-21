import pandas as pd
from valexa.profiles import ProfileManager
import json
import valexa.helper as vx


def ouptut(config):
    config.data = vx.format_json_to_data(config['data'])

    profiles = ProfileManager(config)

    profiles.make_profiles()

    profiles = profiles.output_profiles()
    print(json.dumps({"type": "PROFILE", "data": "START"}))
    for profile in profiles.values():
        print(json.dumps({"type": "PROFILE", "data": profile}))
    print(json.dumps({"type": "PROFILE", "data": "STOP"}))
