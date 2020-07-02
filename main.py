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
    data = sample_dataset.dataset("feinberg_coli")

    data["Validation"]["x"] = np.log10(data["Validation"]["x"])
    data["Validation"]["y"] = np.log10(data["Validation"]["y"])
    for level in data["Validation"]["Level"].unique():
        data["Validation"].loc[data["Validation"]["Level"] == level, "x"] = np.median(
            data["Validation"][data["Validation"]["Level"] == level]["x"]
        )

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        acceptance_limit=0.3,
        rolling_data=False,
        optimizer_parameter=optimizer_parameter,
        allow_correction=True,
        absolute_acceptance=True
    )
    profiles.make_profiles(["1/X Weighted Linear"])
    # profiles.optimize()

    aa = profiles.output_profiles()
    profiles.best().make_plot()
    pass


if __name__ == "__main__":
    main()
