import pytest

from valexa.core.profiles import make_profiles, Profile
from valexa.core.standard import Result


@pytest.fixture()
def calib_data():
    return [
        (1, 1, 0.1, 0.012),
        (1, 2, 5.0, 0.68),
        (1, 3, 10.0, 1.34),
        (2, 1, 0.1, 0.013),
        (2, 2, 5.0, 0.70),
        (2, 3, 10.0, 1.42),

    ]


@pytest.fixture()
def valid_data():
    return [
        (1, 1, 0.1, 0.013),
        (1, 2, 5.0, 0.70),
        (1, 3, 10.0, 1.24),
        (2, 1, 0.1, 0.016),
        (2, 2, 5.0, 0.72),
        (2, 3, 10.0, 1.37),

    ]


def test_make_profiles_returns_profiles(calib_data, valid_data):
    profiles = make_profiles(calib_data, valid_data)

    assert profiles


class TestProfile:
    results_without_repetition = [
        Result(1, 1, 0.1, 0.09),
        Result(1, 2, 5.0, 5.1),
        Result(1, 3, 10.0, 10.5),
        Result(2, 1, 0.1, 0.11),
        Result(2, 2, 5.0, 5.0),
        Result(2, 3, 10.0, 10.4),
    ]

    results_with_repetition = [
        Result(1, 1, 0.1, 0.09),
        Result(1, 1, 0.1, 0.08),
        Result(1, 2, 5.0, 5.1),
        Result(1, 2, 5.0, 5.2),
        Result(1, 3, 10.0, 10.5),
        Result(1, 3, 10.0, 10.4),
        Result(2, 1, 0.1, 0.11),
        Result(2, 1, 0.1, 0.10),
        Result(2, 2, 5.0, 5.0),
        Result(2, 2, 5.0, 5.1),
        Result(2, 3, 10.0, 10.4),
        Result(2, 3, 10.0, 10.2),
    ]

    @pytest.fixture()
    def model_results(self):
        return self.results_without_repetition

    def test_create_from_a_model_results_calculate_levels_from_series(self, model_results):
        profile = Profile(model_results)

        assert len(profile.levels) == 3
        assert len(profile.levels[0].series) == 2

    @pytest.mark.parametrize("model_results", [results_without_repetition, results_with_repetition],
                             ids=["without_rep", "with_rep"])
    def test_calculate_generate_values_to_make_accuracy_profile(self, model_results):
        profile = Profile(model_results)

        profile.calculate()

        for l in profile.levels:
            assert l.introduced_concentration
            assert l.calculated_concentration
            assert l.bias is not None
            assert l.relative_bias is not None
            assert l.recovery
            assert l.repeatability_var is not None
            assert l.repeatability_std is not None
            assert l.inter_series_var is not None
            assert l.inter_series_std is not None
            assert l.absolute_tolerance
            assert l.relative_tolerance
