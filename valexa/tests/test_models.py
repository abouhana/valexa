import pytest

from valexa.core.models import ModelHandler, Model, Result


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

    def test_models_handler_create_models_from_calibration_data(
        self, std_calib, std_valid
    ):
        max_degree = 2
        model_handler = ModelHandler(std_calib, std_valid)

        models = model_handler.get_models(max_degree=max_degree)

        assert len(models) == max_degree
        assert isinstance(models[0], Model)
        assert models[0].series_params
        assert len(models[0].series_calculated) == 6


class TestModel:
    def test_name_property(self):
        degree = 1
        model = Model()
        model.degree = degree

        name = model.name

        assert name == Model.NAME_BY_DEGREE[degree]

    @pytest.fixture()
    def results_with_shift(self):
        return [
            Result(1, 1, 10.0, 8.0),
            Result(1, 2, 20.0, 16.0),
            Result(2, 1, 10.0, 7.5),
            Result(2, 2, 20.0, 17.0),
        ]

    @pytest.fixture()
    def model_with_shift(self, results_with_shift):
        model = Model()
        model.series_calculated = results_with_shift

        return model

    def test_correction_detection(self, model_with_shift: Model):
        model_with_shift.handle_correction()

        assert model_with_shift.has_correction
        assert model_with_shift.correction_factor == round(1 / 0.8, 1)

    def test_apply_correction_factor_to_result(
        self, model_with_shift: Model, results_with_shift
    ):
        model_with_shift.handle_correction()

        correction_factor = model_with_shift.correction_factor
        for (index, s) in enumerate(model_with_shift.series_calculated):
            assert s.result == results_with_shift[index].result * correction_factor
