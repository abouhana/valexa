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
