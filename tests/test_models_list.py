from valexa.models_list import model_list
import pytest


class TestModelsList:
    def test_model_list_return_single_model(self):
        model = model_list("Linear")
        assert model == {"formula": "y ~ x", "weight": None, "min_points": 2}

    def test_model_list_return_all_models(self):
        model = model_list()
        assert isinstance(model, dict)

    def test_model_list_error(self):
        with pytest.raises(KeyError):
            model_list("")
