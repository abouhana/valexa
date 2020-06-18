from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset

import pandas as pd


def test_feinberg_nicotinamide():
    """
    Dataset from:
    Feinberg, M., Labo-Stat (2010), https://www.lavoisier.fr/livre/sciences-de-la-vie/labo-stat/feinberg/descriptif-9782743014261
    Feinberg, M., Validation of analytical methods based on accuracy profiles, https://www.sciencedirect.com/science/article/abs/pii/S0021967307002804


    This is an example of validation with a linear calibration curve made before every series and correction factor.

    The reference DataFrame for the model is as follow:

     Serie | Slope  | Origin
    -------+--------+--------
     1     | 70.986 | -5.494
    -------+--------+--------
     2     | 69.875 | -5.100
    -------+--------+--------
     3     | 69.167 | -5.767

    Note: There seems to be a disrepancy between the value shown in the book and the value calculated by Valexa. This
    may be explained by rounding error in Excel.
    """
    data = sample_dataset.dataset("feinberg_nicotinamide")

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        acceptance_limit=10,
        tolerance_limit=80,
        model_to_test="Linear"
    )
    profiles.make_profiles()

    litterature_model_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "Slope": {
                1: 70.986,
                2: 69.875,
                3: 69.167
            },
            "Origin": {
                1: -5.494,
                2: -5.100,
                3: -5.767
            }
        }
    )
    litterature_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "repeatability_std": {
                1: 0.0058,
                2: 0.0296,
                3: 0.0816
            },
            "inter_series_std": {
                1: 0.0153,
                2: 0.0442,
                3: 0.0281
            },
            "tolerance_std": {
                1: 0.0187,
                2: 0.0598,
                3: 0.0919
            },
            "bias": {
                1: 2.3,
                2: 0.5,
                3: -1.1
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

    #assertion_dataframe: pd.DataFrame = profiles.profiles["Direct"][0].get_profile_parameter(["repeatability_std",
    #                                                                                          "inter_series_std",
    #                                                                                          "tolerance_std",
    #                                                                                          "bias"]).round(3)

    #assertion_dataframe[["abs_tolerance_low", "abs_tolerance_high"]] = pd.DataFrame(
    #    profiles.profiles["Direct"][0].get_profile_parameter(["abs_tolerance"]).abs_tolerance.tolist(),
    #    index=assertion_dataframe.index
    #).round(3)

    assert assertion_dataframe.equals(litterature_dataframe)