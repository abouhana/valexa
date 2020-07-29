from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset
import valexa.helper as vx
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
    data = sample_dataset.dataset("inra_pyrene")


    config = {
        "compound_name": "Test",
        "rolling_data": True,
        "optimizer_parameter": optimizer_parameter,
        "correction_allow": False,
        "data": data,
        "model_to_test": "1/X^2 Weighted Linear",
        "rolling_limit": 3,
        "significant_figure": 4,


    }

    config = json.loads('{"compound_name":"Pyrene","data":{"validation":[{"series":1,"level":1,"x":1.9,"y1":36539,"y2":36785},{"series":2,"level":1,"x":1.9,"y1":60086,"y2":35295},{"series":3,"level":1,"x":1.9,"y1":57695,"y2":59731},{"series":1,"level":2,"x":4.7,"y1":102066,"y2":98495},{"series":2,"level":2,"x":4.7,"y1":99897,"y2":93547},{"series":3,"level":2,"x":4.7,"y1":115298,"y2":111584},{"series":1,"level":3,"x":9.5,"y1":188665,"y2":191294},{"series":2,"level":3,"x":9.5,"y1":188657,"y2":198683},{"series":3,"level":3,"x":9.5,"y1":221678,"y2":194983},{"series":1,"level":4,"x":28.5,"y1":595999,"y2":604704},{"series":2,"level":4,"x":28.5,"y1":520857,"y2":501025},{"series":3,"level":4,"x":28.5,"y1":557258,"y2":541355}],"calibration":[{"series":1,"level":1,"x":0.9,"y1":43083},{"series":2,"level":1,"x":0.9,"y1":24719},{"series":3,"level":1,"x":0.9,"y1":35684},{"series":1,"level":2,"x":4.6,"y1":117767},{"series":2,"level":2,"x":4.6,"y1":112319},{"series":3,"level":2,"x":4.6,"y1":115840},{"series":1,"level":3,"x":9.2,"y1":238120},{"series":2,"level":3,"x":9.2,"y1":202957},{"series":3,"level":3,"x":9.2,"y1":249807},{"series":1,"level":4,"x":18.4,"y1":450132},{"series":2,"level":4,"x":18.4,"y1":398342},{"series":3,"level":4,"x":18.4,"y1":440029},{"series":1,"level":5,"x":27.6,"y1":682393},{"series":2,"level":5,"x":27.6,"y1":611523},{"series":3,"level":5,"x":27.6,"y1":633748}]},"tolerance_limit":80,"acceptance_limit":20,"acceptance_absolute":false,"quantity_units":null,"rolling_data":true,"rolling_limit":3,"model_to_test":"1/X^2 Weighted Linear","generate_figure":false,"correction_allow":false,"correction_threshold":[0.9,1.1],"correction_forced_value":1,"correction_round_to":2,"optimizer_parameter":null,"significant_figure":4,"stats":""}')
    config['data'] = vx.format_json_to_data(config['data'])

    profiles = ProfileManager(**config)
    profiles.make_profiles()
    # profiles.optimize()

    aa = profiles.output_profiles()

    for zz in aa.values():
        print(json.dumps({"type": "PROFILE", "data": zz}))

    profiles.optimize()

    pass

if __name__ == "__main__":
    main()

