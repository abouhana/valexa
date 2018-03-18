import pytest

from valexa.core.standard import Standard


class TestStandard:

    @pytest.fixture()
    def calib_data(self):
        return [
            (1, 1, 0.1, 0.012),
            (1, 2, 5.0, 0.68),
            (1, 3, 10.0, 1.34),
            (2, 1, 0.1, 0.013),
            (2, 2, 5.0, 0.70),
            (2, 3, 10.0, 1.42),

        ]

    @pytest.fixture()
    def valid_data(self):
        return [
            (1, 1, 0.1, 0.013),
            (1, 2, 5.0, 0.70),
            (1, 3, 10.0, 1.24),
            (2, 1, 0.1, 0.016),
            (2, 2, 5.0, 0.72),
            (2, 3, 10.0, 1.37),

        ]

    def test_split_values_by_series_on_init(self, calib_data):
        std = Standard(calib_data)

        assert len(std.series.keys()) == 2
        assert len(std.series[1]) == 3

    @pytest.mark.parametrize("degree,expected", [
        (3, 3),
        (1, 1),
        (2, 2),
    ])
    def test_get_models_parameters_return_parameters_by_models(self, calib_data, degree, expected):
        std = Standard(calib_data)

        models_parameters = std.get_models_parameters(max_degree=degree)

        assert len(models_parameters) == expected

    def test_apply_models_parameters_returns_result_by_model(self, calib_data, valid_data):
        std_calib = Standard(calib_data)
        std_valid = Standard(valid_data)
        models_parameters = std_calib.get_models_parameters(max_degree=3)

        models_results = std_valid.apply_models(models_parameters)

        assert len(models_results) == 3
