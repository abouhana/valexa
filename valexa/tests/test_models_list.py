from valexa.core.models_list import model_list


def test_model_list_return_single_model():
    model = model_list("Linear")
    assert model == {"formula": "y ~ x", "weight": None}


def test_model_list_return_all_models():
    model = model_list()
    assert isinstance(model, dict)
