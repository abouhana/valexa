from core.profiles import ProfileManager
from examples.data import sample_dataset
import numpy as np


def test_feinberg_coli():
    """
    Dataset from Feinberg, M. et al., Validation of Alternative Methods for the Analysis of Drinking Water and Their
    Application to Escherichia coli (2011), https://dx.doi.org/10.1128/AEM.00020-11
    This is an example of validation with absolute unit, in this case a bacterial count.
    Here the raw data are manipulated before being passed to the algorithm. They are transformed in their log10
    equivalent and the target level are using the median instead of the mean. Please refer to the article for more
    information.
    """
    data = sample_dataset.dataset("feinberg_coli")

    data["Validation"]["x"] = np.log10(data["Validation"]["x"])
    data["Validation"]["y"] = np.log10(data["Validation"]["y"])
    for level in data["Validation"]["Level"].unique():
        data["Validation"].loc[data["Validation"]["Level"] == level,"x"] = \
            np.median(data["Validation"][data["Validation"]["Level"] == level]["x"])


    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        absolute_acceptance=True,
        acceptance_limit=0.3
    )
    profiles.make_profiles()
    profiles.profiles["Direct"][0].get_profile_parameter(["bias", "abs_tolerance"])

    assert True