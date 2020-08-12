from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset


def test_intern_dataset():
    """
    This dataset is internal and is mainly use to show some of the other parameter for the profile manager such as:
    - rolling_data - Which will generate all potential profile in a dataset.
    - generate_figure - Which will generate figure for all profiles automatically (may generate error if more than 25
    profiles are generated, this is a limitation of matplotlib)
    - optimize and optimizer_paramater - An experimental function that will sort the generated profile based on
    specified parameters.
    :return:
    """
    optimizer_parameter = {
        "has_limits": True,
        "validation_range": "max",
        "average.bias_abs": "min",
        "min_loq": "min",
        "model.rsquared": "max",
    }
    data = sample_dataset.dataset("intern_test")

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        model_to_test="Linear",
        rolling_data=True,
        optimizer_parameter=optimizer_parameter,
        correction_allow=True,
    )
    profiles.make_profiles(["Linear"])
    profiles.optimize()

    profiles.profiles["Linear"][1].summary()

    return True


if __name__ == "__main__":
    test_intern_dataset()
