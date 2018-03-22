import pytest

from valexa.core.models import ModelHandler, Model
from valexa.core.standard import Standard


class TestModelHandler:
    @pytest.fixture()
    def std_calib(self):
        data = [
            (1, 1, 0.1, 0.012),
            (1, 2, 5.0, 0.68),
            (1, 3, 10.0, 1.34),
            (2, 1, 0.1, 0.013),
            (2, 2, 5.0, 0.70),
            (2, 3, 10.0, 1.42),

        ]
        return Standard(data)

    @pytest.fixture()
    def std_valid(self):
        data = [
            (1, 1, 0.1, 0.013),
            (1, 2, 5.0, 0.70),
            (1, 3, 10.0, 1.24),
            (2, 1, 0.1, 0.016),
            (2, 2, 5.0, 0.72),
            (2, 3, 10.0, 1.37),

        ]
        return Standard(data)

    def test_models_handler_create_models_from_calibration_data(self, std_calib, std_valid):
        max_degree = 2
        model_handler = ModelHandler(std_calib, std_valid)

        models = model_handler.get_models(max_degree=max_degree)

        assert len(models) == max_degree
        assert isinstance(models[0], Model)
        assert models[0].series_params
        assert len(models[0].series_calculated) == 6
