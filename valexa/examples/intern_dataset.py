from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset

def test_intern_dataset():
    optimizer_parameter = {
        "has_limits": True,
        "validation_range": "max",
        "average.bias": "min",
        "min_loq": "min",
        "model.rsquared": "max",
    }
    data = sample_dataset.dataset("intern_test")

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        model_to_test="Linear",
        rolling_data=True,
        absolute_acceptance=True,
        acceptance_limit=20,
        optimizer_parameter=optimizer_parameter,
        allow_correction=True
    )
    profiles.make_profiles(["Linear"])
    profiles.optimize()

    assert len(profiles.sorted_profiles) == 2
    return True

