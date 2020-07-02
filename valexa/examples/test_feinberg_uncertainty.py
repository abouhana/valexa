from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset

import pandas as pd
import numpy as np


def test_feinberg_uncertainty():
    """
    Dataset from:
    Feinberg et al. (2004) New advances in method validation and measurement uncertainty aimed at improving the quality
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
        significant_figure=5,
    )
    profiles.make_profiles()

    literature_composite_uncertainty = pd.DataFrame(
        {1: 1.399, 2: 20.628, 3: 36.385}, index=["tolerance_std"]
    ).transpose()

    literature_relative_expanded_uncertainty = pd.DataFrame(
        {1: 11.0, 2: 9.4, 3: 8.7}, index=["uncertainty_pc"]
    ).transpose()

    calculated_composite_uncertainty = profiles.best().get_profile_parameter(
        "tolerance_std"
    )

    calculated_relative_expanded_uncertainty = profiles.best().get_profile_parameter(
        "uncertainty_pc"
    )

    # We calculate an assertion matrix based on the percentage of error from the literature value, for those in
    # absolute unit

    composite_uncertainty_assertion = np.abs(
        calculated_composite_uncertainty.sub(literature_composite_uncertainty).divide(
            literature_composite_uncertainty
        )
        * 100
    )

    # We calculate an assertion matrix based on the difference in percentage from the literature value, for already in
    # percentage

    relative_expanded_uncertainty_assertion = np.abs(
        calculated_relative_expanded_uncertainty.sub(
            literature_relative_expanded_uncertainty
        )
    )

    # We accept a maximum of 2.5% deviation from the literature value. This is mainly due to rounding error

    assert composite_uncertainty_assertion.ge(2.5).any() is not True
    assert relative_expanded_uncertainty_assertion.ge(0.25).any() is not True

    return True
