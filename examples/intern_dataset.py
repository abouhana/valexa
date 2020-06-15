from core.profiles import ProfileManager
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
    data = sample_dataset.dataset("feinberg_coli")

    data["Validation"]["x"] = np.log10(data["Validation"]["x"])
    data["Validation"]["y"] = np.log10(data["Validation"]["y"])
    for level in data["Validation"]["Level"].unique():
        data["Validation"].loc[data["Validation"]["Level"] == level,"x"] = np.median(data["Validation"][data["Validation"]["Level"] == level]["x"])


    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        absolute_acceptance=True,
        acceptance_limit=0.3
    )
    print("--- %s seconds ---" % (time.time() - start_time))
    profiles.make_profiles(["Linear", "Quadratic"])
    print("--- %s seconds ---" % (time.time() - start_time))
    profiles.optimize()
    print("--- %s seconds ---" % (time.time() - start_time))

    exit()
