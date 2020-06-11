from core.profiles import ProfileManager
from tests.data import test_dataset

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
    profiles: ProfileManager = ProfileManager(
        "Test",
        test_dataset.dataset("intern_test"),
        rolling_data=True,
        allow_correction=True,
        forced_correction_value=1.2,
        optimizer_parameter=optimizer_parameter,
    )
    print("--- %s seconds ---" % (time.time() - start_time))
    profiles.make_profiles(["Linear", "Quadratic"])
    print("--- %s seconds ---" % (time.time() - start_time))
    profiles.optimize()
    print("--- %s seconds ---" % (time.time() - start_time))

    exit()
