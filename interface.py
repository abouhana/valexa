import json
from valexa.profiles import ProfileManager
from valexa.examples.dataset.sample_dataset import dataset
import pandas as pd
import numpy as np
import os
import pathlib


def main():
    data = dataset("sfstp")

    val = data["Validation"].to_dict()
    cal = data["Calibration"].to_dict()

    print(json.dumps({"Validation": val, "Calibration": cal}))

    aa = ProfileManager("Test", data, absolute_acceptance=True, acceptance_limit=0.3)
    aa.make_profiles()

    os.wait(5)

    while( True ):
        input_stream = input()
        print(input_stream)


if __name__ == '__main__':
    main()
    print("Clean exit")
    sys.stdout.flush()
