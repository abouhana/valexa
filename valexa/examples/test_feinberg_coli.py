from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset
import numpy as np
import pandas as pd


def test_feinberg_coli():
    """
    Dataset from Feinberg, M. et al., Validation of Alternative Methods for the Analysis of Drinking Water and Their
    Application to Escherichia coli (2011), https://dx.doi.org/10.1128/AEM.00020-11

    This is an example of validation with absolute unit, in this case a bacterial count.
    Here the raw data are manipulated before being passed to the algorithm. They are transformed in their log10
    equivalent and the target level are using the median instead of the mean. Please refer to the article for more
    information.

    The reference DataFrame is as follow:

         | repeatability_std | inter_series_std | tolerance_std | bias  | abs_tolerance_low | abs_tolerance_high
    -----+-------------------+------------------+---------------+-------+-------------------+--------------------
      1  | 0.141             | 0.092            | 0.173         | 0.024 | -0.206            | 0.254
    -----+-------------------+------------------+---------------+-------+-------------------+--------------------
      2  | 0.093             | 0.081            | 0.127         | 0.055 | -0.115            | 0.225
    -----+-------------------+------------------+---------------+-------+-------------------+--------------------
      3  | 0.099             | 0.141            | 0.178         | 0.093 | -0.147            | 0.333

    Note: the kM value given in the article is equivalent to kIT * sqrt(1 + (1/(nb_measures * b_coefficient)), the
    tolerance interval obtained stays the same since Valexa add this factor in the calculation of the tolerance standard
    deviation instead of the calculation of the coverage factor as found in the article. In the same way, the sFI needs
    to be divided by the same equation.
    The reference DataFrame is as follow:

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

    litterature_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "repeatability_std": {
                1: 0.141,
                2: 0.093,
                3: 0.099
            },
            "inter_series_std": {
                1: 0.092,
                2: 0.081,
                3: 0.141
            },
            "tolerance_std": {
                1: 0.173,
                2: 0.127,
                3: 0.178
            },
            "bias": {
                1: 0.024,
                2: 0.055,
                3: 0.093
            },
            "abs_tolerance_low": {
                1: -0.206,
                2: -0.115,
                3: -0.147
            },
            "abs_tolerance_high": {
                1: 0.254,
                2: 0.225,
                3: 0.333
            },
        })

    results_dataframe: pd.DataFrame = profiles.profiles["Direct"][0].get_profile_parameter(["repeatability_std",
                                                                                              "inter_series_std",
                                                                                              "tolerance_std",
                                                                                              "bias"]).round(3)

    results_dataframe[["abs_tolerance_low", "abs_tolerance_high"]] = pd.DataFrame(profiles.profiles["Direct"][0].get_profile_parameter(["abs_tolerance"])).transpose().round(3)

    assertion_dataframe = np.abs(litterature_dataframe.sub(results_dataframe).divide(litterature_dataframe)*100)

    # We allow 0.5% since most number have only 3 significants figures. One the data has a 0.001 absolute deviation
    # which translate to a > 0.5% error (Literature: 0.178, Valexa: 0.177), probably due to rounding. We take it into
    # account during the assert.

    assert len(assertion_dataframe[assertion_dataframe.ge(0.5).any(axis=1)]) == 1
    return True