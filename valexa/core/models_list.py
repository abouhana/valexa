from typing import Union, Dict, Optional

ModelInfo = Dict[str, Optional[str]]


def model_list(model_name: str = "") -> Union[ModelInfo, Dict[str, ModelInfo]]:
    """
    This function simply return a hardcoded list of model or the informaion on a single model.
    It can be modified to include new model. The required format is the following:
    Name of the model string: {
        "formula": mathematical formula string using the Patsy format,
        "weight": None or a mathematical expression in the sympy format
    }
    :type model_name: Name of the model to return
    """
    model_list_var = {
        "Linear": {
            "formula": "y ~ x",
            "weight": None,
        },
        "Linear though 0": {
            "formula": "y ~ x - 1",
            "weight": None,
        },
        "Quadratic": {
            "formula": "y ~ x + I(x**2)",
            "weight": None,
        },
        "1/X Weighted Linear": {
            "formula": "y ~ x",
            "weight": "1/x",
        },
        "1/X^2 Weighted Linear": {
            "formula": "y ~ x",
            "weight": "1/x**2",
        },
        "1/Y Weighted Linear": {
            "formula": "y ~ x",
            "weight": "1/y",
        },
        "1/Y^2 Weighted Linear": {
            "formula": "y ~ x",
            "weight": "1/y**2",
        },
        "1/X Weighted Quadratic": {
            "formula": "y ~ x + I(x**2)",
            "weight": "1/x",
        },
        "1/X^2 Weighted Quadratic": {
            "formula": "y ~ x + I(x**2)",
            "weight": "1/x**2",
        },
        "1/Y Weighted Quadratic": {
            "formula": "y ~ x + I(x**2)",
            "weight": "1/y",
        },
        "1/Y^2 Weighted Quadratic": {
            "formula": "y ~ x + I(x**2)",
            "weight": "1/y**2",
        }
    }

    if model_name == "":
        return model_list_var
    else:
        return model_list_var[model_name]
