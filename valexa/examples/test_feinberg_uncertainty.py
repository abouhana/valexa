from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset

import pandas as pd
import numpy as np


def test_feinberg_uncertainty():
    """
    Dataset from:
    Feinbger et al. (2004) New advances in method validation and measurement uncertainty aimed at improving the quality
        of chemical data. https://dx.doi.org/10.1007/s00216-004-2791-y

    This dataset is used to verify that the uncertainty calculation is in accordance with the literature.
    """
    data = sample_dataset.dataset("feinberg_uncertainty")

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        acceptance_limit=20,
        tolerance_limit=90,
        model_to_test=["1/X^2 Weighted Linear"],
    )
    profiles.make_profiles()


    literature_composite_uncertainty: pd.Series = pd.Series(
        {
            1: 1.399,
            2: 20.628,
            3: 36.385
        }
    )

    literature_relative_expanded_uncertainty: pd.Series = pd.Series(
        {
            1: 11.0,
            2: 9.4,
            3: 8.7
        }
    )

    calculated_composite_uncertainty: pd.Series = pd.Series(
        profiles.profiles["1/X^2 Weighted Linear"][0].get_profile_parameter("tolerance_std")
    )

    calculated_relative_expanded_uncertainty: pd.Series = pd.Series(
        profiles.profiles["1/X^2 Weighted Linear"][0].get_profile_parameter("pc_uncertainty")
    )


    # We calculate an assertion matrice based on the percentage of error from the litterature value, for those in
    # absolute unit

    composite_uncertainty_assertion = np.abs(
        calculated_composite_uncertainty.sub(literature_composite_uncertainty).divide(literature_composite_uncertainty)*100
    )

    # We calculate an assertion matrice based on the difference in percentage from the litterature value, for already in
    # percentage

    relative_expanded_uncertainty_assertion = np.abs(calculated_relative_expanded_uncertainty.sub(literature_relative_expanded_uncertainty))


    # We accept a maximum of 5% deviation from the literature value. This is mainly due to rounding error

    assert composite_uncertainty_assertion.ge(5).any() is not True
    assert relative_expanded_uncertainty_assertion.ge(0.5).any() is not True

    return True
