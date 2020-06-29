from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset
import numpy as np


def main():
    """
    Dataset from:
    inra_pyrene: Huyez-Levrat, M et al.,Cahier technique de l'INRA - Validation des méthodes (2010), https://www6.inrae.fr/cahier_des_techniques/Les-Cahiers-parus/Les-n-Speciaux-et-les-n-Thematiques/Validation-des-methodes

    This dataset is mainly use to check if the correction factor generated is 1.2.
    The
    :return:
    """

    optimizer_parameter = {
        "has_limits": True,
        "validation_range": "max",
        "average.bias_abs": "min",
        "min_loq": "min",
        "model.rsquared": "max",
    }
    data = sample_dataset.dataset("sfstp")

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        rolling_data=True,
        optimizer_parameter=optimizer_parameter,
        allow_correction=True,
    )
    profiles.make_profiles(["Linear"])
    profiles.optimize()

    profiles.profiles["Linear"][1].summary()

    pass


if __name__ == '__main__':
    main()