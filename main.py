from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset
import numpy as np
import json


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

    config = {
        "compound_name": "Test",
        "rolling_data": False,
        "optimizer_parameter": optimizer_parameter,
        "allow_correction": True
    }

    profiles: ProfileManager = ProfileManager(
        data=data, **config

    )
    profiles.make_profiles(["Linear","Quadratic"])
    # profiles.optimize()

    aa = profiles.output_profiles()

    for zz in aa.values():
        print(json.dumps({"type": "PROFILE", "data": zz}))

    profiles.optimize()

    pass

if __name__ == "__main__":
    main()

