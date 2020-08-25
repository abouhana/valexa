from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset
from plotly.utils import PlotlyJSONEncoder
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
    data = sample_dataset.dataset("sfstp")


    config = {
        "compound_name": "Test",
        "rolling_data": False,
        "optimizer_parameter": optimizer_parameter,
        "correction_allow": True,
        "data": data,
        "model_to_test": "Linear",
        "rolling_limit": 3,
        "significant_figure": 4,
    }

    config = json.loads('{"compound_name":"template","data":{"validation":[{"series":1,"level":1,"x":" 1.9","y1":36539,"y2":36785,"$id":"15063999-0000000"},{"series":1,"level":2,"x":" 4.7","y1":102066,"y2":98495,"$id":"15063999-0000001"},{"series":1,"level":3,"x":" 9.5","y1":188665,"y2":191294,"$id":"15063999-0000002"},{"series":1,"level":4,"x":" 28.5","y1":595999,"y2":604704,"$id":"15063999-0000003"},{"series":2,"level":1,"x":" 1.9","y1":60086,"y2":35295,"$id":"15063999-0000004"},{"series":2,"level":2,"x":" 4.7","y1":99897,"y2":93547,"$id":"15063999-0000005"},{"series":2,"level":3,"x":" 9.5","y1":188657,"y2":198683,"$id":"15063999-0000006"},{"series":2,"level":4,"x":" 28.5","y1":520857,"y2":501025,"$id":"15063999-0000007"},{"series":3,"level":1,"x":" 1.9","y1":57695,"y2":59731,"$id":"15063999-0000008"},{"series":3,"level":2,"x":" 4.7","y1":115298,"y2":111584,"$id":"15063999-0000009"},{"series":3,"level":3,"x":" 9.5","y1":221678,"y2":194983,"$id":"15063999-0000010"},{"series":3,"level":4,"x":" 28.5","y1":557258,"y2":541355,"$id":"15063999-0000011"}],"calibration":[{"series":1,"level":1,"x":" 0.9","y1":43083,"y2":24719,"y3":35684,"$id":"15064008-0000000"},{"series":1,"level":2,"x":" 4.6","y1":117767,"y2":112319,"y3":115840,"$id":"15064008-0000001"},{"series":1,"level":3,"x":" 9.2","y1":238120,"y2":202957,"y3":249807,"$id":"15064008-0000002"},{"series":1,"level":4,"x":" 18.4","y1":450132,"y2":398342,"y3":440029,"$id":"15064008-0000003"},{"series":1,"level":5,"x":" 27.6","y1":682393,"y2":611523,"y3":633748,"$id":"15064008-0000004"}]},"tolerance_limit":80,"acceptance_limit":20,"acceptance_absolute":false,"quantity_units":null,"rolling_data":false,"rolling_limit":3,"model_to_test":"Linear","correction_allow":true,"correction_threshold":[0.9,1.1],"correction_forced_value":null,"correction_round_to":2,"optimizer_parameter":null,"significant_figure":4,"lod_allowed":null,"lod_force_miller":false,"status":""}')
    config['data'] = vx.format_json_to_data(config['data'])
    # config['correction_allow'] = True
    # config['correction_forced_value'] = None

    profiles = ProfileManager(**config)
    profiles.make_profiles()
    # profiles.optimize()


    aa = profiles.output_profiles()

    for zz in aa.values():
        print(json.dumps({"type": "PROFILE", "data": zz}, cls=PlotlyJSONEncoder))

    profiles.optimize()

    pass

if __name__ == "__main__":
    main()

