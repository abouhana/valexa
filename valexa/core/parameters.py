from enum import Enum


class Quantity(Enum):
    CONCENTRATION = "conc"
    AMOUNT = "amount"
    RELATIVE_VALUE = "rel_val"


class ValidationParameters:
    def __init__(self):
        self.quantity: Quantity = Quantity.CONCENTRATION.value
        self.introduction_unit = ""
        self.response_signal_unit = ""
        self.acceptance_limit = 0.20
        self.tolerance_limit = 0.80
