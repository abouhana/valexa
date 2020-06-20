from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset

import pandas as pd
import numpy as np

def test_feinberg_labostat():
    """
    Dataset from:
    Feinberg, M., Labo-Stat (2010), https://www.lavoisier.fr/livre/sciences-de-la-vie/labo-stat/feinberg/descriptif-9782743014261

    The reference DataFrame for the model is as follow:

     Serie | x      | Intercept
    -------+--------+--------
     1     | 70.986 | -5.494
    -------+--------+--------
     2     | 69.875 | -5.100
    -------+--------+--------
     3     | 69.167 | -5.767

    Note: There seems to be a slight disrepancy in some value, especially for very small one variance, rounding errors
    have a large effect at very low level of variance. For this reason we only assert the recovery, relative tolerance
    interval, the models and the limit of quantification.
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

    literature_model_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "x": {
                1: 70.986,
                2: 69.875,
                3: 69.167
            },
            "Intercept": {
                1: -5.494,
                2: -5.100,
                3: -5.767
            }
        }
    )
    literature_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "recovery": {
                1: 102.3,
                2: 100.5,
                3: 98.9
            },
            "rel_tolerance_low": {
                1: 93.9,
                2: 95.7,
                3: 95.6
            },
            "rel_tolerance_high": {
                1: 110.7,
                2: 105.4,
                3: 102.1
            }
        })

    calculated_model_dict = {}
    for key, value in profiles.profiles["Linear"][0].model.fit.items():
        calculated_model_dict[key] = value.params

    calculated_model_dataframe = pd.DataFrame(calculated_model_dict).transpose().round(3)

    calculated_dataframe: pd.DataFrame = pd.DataFrame(
        profiles.profiles["Linear"][0].get_profile_parameter(["recovery"]), index=["recovery"]).transpose().round(1)

    calculated_dataframe[["rel_tolerance_low", "rel_tolerance_high"]] = pd.DataFrame(
        profiles.profiles["Linear"][0].get_profile_parameter(["rel_tolerance"])).transpose().round(1)

    assertion_dataframe = np.abs(calculated_dataframe.sub(literature_dataframe))
    assertion_model_dataframe = np.abs(calculated_model_dataframe.sub(literature_model_dataframe).div(literature_model_dataframe)*100)


    assert np.abs((0.4473-profiles.profiles["Linear"][0].min_loq)/0.4473*100) < 5
    assert len(assertion_dataframe[assertion_dataframe.ge(1).any(axis=1)]) == 0
    assert len(assertion_model_dataframe[assertion_model_dataframe.ge(0.01).any(axis=1)]) == 0

    return True