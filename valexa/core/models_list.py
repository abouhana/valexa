# Temporary file to store the list of model
# Should be migrated to a SQLite database later during dev

def model_list(model_number:int = 1):
    model_list = {
        1: {
            "name": "Linear",
            "formula": "y ~ x",
            "weight": None,
        },
        2: {
            "name": "Linear though 0",
            "formula": "y ~ x - 1",
            "weight": None,
        },
        3: {
            "name": "Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": None,
        },
        4: {
            "name": "1/X Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/x",
        },
        5: {
            "name": "1/X^2 Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/x**2",
        },
        6: {
            "name": "1/Y Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/y",
        },
        7: {
            "name": "1/Y^2 Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/y**2",
        },
        8: {
            "name": "1/X Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/x",
        },
        9: {
            "name": "1/X^2 Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/x**2",
        },
        10: {
            "name": "1/Y Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/y",
        },
        11: {
            "name": "1/Y^2 Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/y**2",
        }
    }

    return model_list[model_number]