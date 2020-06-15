from valexa.profiles import ProfileManager
from examples.dataset import sample_dataset
import numpy as np

import time

if __name__ == "__main__":
    start_time = time.time()
    optimizer_parameter = {
        "has_limits": True,
        "validation_range": "max",
        "average.bias": "min",
        "min_loq": "min",
        "model.rsquared": "max",
    }
    data = sample_dataset.dataset("inra_pyrene")


    profiles: ProfileManager = ProfileManager(
        "Test",
        data,

    )
    profiles.make_profiles(["Linear", "Quadratic"])

    exit()
