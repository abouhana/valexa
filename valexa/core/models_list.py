# Temporary file to store the list of model
# Should be migrated to a SQLite database later during dev

def model_list(model_name: str = ""):
    model_list = {
        "Linear" : {
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
        return model_list
    else:
        return model_list[model_name]