import numpy as np


def model_list(model_number:int = 1):
    model_list = {
        1: {
            "name": "Linear",
            "formula": "y ~ x",
            "weight": None,
            "solver": "statsmodels"
        },
        2: {
            "name": "Linear though 0",
            "formula": "y ~ x - 1",
            "weight": None,
            "function": "p['x'] * x - p['y']"
        },
        3: {
            "name": "Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": None,
            "function": "p['I(x ** 2)'] * x**2 + p['x'] * x + p['Intercept'] - p['y']"
        },
        4: {
            "name": "1/X Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/x",
            "function": "p['x'] * x + p['Intercept'] - p['y']"
        },
        5: {
            "name": "1/X^2 Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/x**2",
            "function": "p['x'] * x + p['Intercept'] - p['y']"
        },
        6: {
            "name": "1/Y Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/y",
            "function": "p['x'] * x + p['Intercept'] - p['y']"
        },
        7: {
            "name": "1/Y^2 Weighted Linear",
            "formula": "y ~ x",
            "weight": "1/y**2",
            "function": "p['x'] * x + p['Intercept'] - p['y']"
        },
        8: {
            "name": "1/X Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/x",
            "function": "p['I(x ** 2)'] * x**2 + p['x'] * x + p['Intercept'] - p['y']"
        },
        9: {
            "name": "1/X^2 Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/x**2",
            "function": "p['I(x ** 2)'] * x**2 + p['x'] * x + p['Intercept'] - p['y']"
        },
        10: {
            "name": "1/Y Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/y",
            "function": "p['I(x ** 2)'] * x**2 + p['x'] * x + p['Intercept'] - p['y']"
        },
        11: {
            "name": "1/Y^2 Weighted Quadratic",
            "formula": "y ~ x + I(x**2)",
            "weight": "1/y**2",
            "function": "p['I(x ** 2)'] * x**2 + p['x'] * x + p['Intercept'] - p['y']"
        }
    }

    return model_list[model_number]