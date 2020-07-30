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
        "model_to_test": "Linear",
        "rolling_limit": 3,
        "significant_figure": 4,


    }

    config = json.loads('{"compound_name":"Deltamethrin Sum","data":{"validation":[{"series":1,"level":1,"x":1,"y1":758.494108905246,"y2":2024.3126011938,"y3":1485.98188501412},{"series":1,"level":2,"x":2.5,"y1":4951.82705946931,"y2":2945.99924878414,"y3":3381.53233004891},{"series":1,"level":3,"x":5,"y1":2569.65101487864,"y2":7223.05480008645,"y3":7604.90690000712},{"series":1,"level":4,"x":10,"y1":11979.4312282624,"y2":10959.2487822055,"y3":12294.4926204644},{"series":1,"level":5,"x":25,"y1":32139.8794254361,"y2":31180.0700677758,"y3":36770.2908862747},{"series":2,"level":1,"x":1,"y1":738.588986726812,"y2":927.082136921978,"y3":834.422912743264},{"series":2,"level":2,"x":2.5,"y1":2399.67712397508,"y2":1958.83074162228,"y3":1714.81213457624},{"series":2,"level":3,"x":5,"y1":4981.97045132126,"y2":5609.74551998124,"y3":5397.71216282476},{"series":2,"level":4,"x":10,"y1":10337.3390110217,"y2":10888.910778458,"y3":13327.5703732737},{"series":2,"level":5,"x":25,"y1":27387.7973402733,"y2":27638.4179768726,"y3":31408.3213505348},{"series":3,"level":1,"x":1,"y1":996.377068290235,"y2":575.123218758911,"y3":1132.50639422323},{"series":3,"level":2,"x":2.5,"y1":2002.08757526943,"y2":1938.99861612391,"y3":3254.44360987088},{"series":3,"level":3,"x":5,"y1":4659.07158236478,"y2":4822.91953141,"y3":6808.1522193042},{"series":3,"level":4,"x":10,"y1":5813.03045643409,"y2":6708.31658125904,"y3":9531.17058766422},{"series":3,"level":5,"x":25,"y1":19653.9547479073,"y2":20800.7866538919,"y3":34621.2847847259}],"calibration":[{"series":1,"level":1,"x":1,"y1":35.8370614462758,"y2":35.6707822771837,"y3":19.7074078002249},{"series":1,"level":2,"x":2.5,"y1":123.217163307592,"y2":194.412463524815,"y3":98.7459072705493},{"series":1,"level":3,"x":5,"y1":479.100576158449,"y2":641.952086685202,"y3":809.679748018884},{"series":1,"level":4,"x":10,"y1":1104.25660181007,"y2":1136.78627228355,"y3":872.442943545285},{"series":1,"level":5,"x":25,"y1":2418.08120729499,"y2":3254.24642548976,"y3":3276.83438815066},{"series":2,"level":1,"x":1,"y1":43.8727235077404,"y2":39.8237386674237,"y3":24.8487016888258},{"series":2,"level":2,"x":2.5,"y1":56.4487694539486,"y2":38.8991784146109,"y3":28.1965092724022},{"series":2,"level":3,"x":5,"y1":85.1924819683729,"y2":89.7357395059618,"y3":150.764621120218},{"series":2,"level":4,"x":10,"y1":564.797388092028,"y2":718.413282596009,"y3":945.12484236471},{"series":2,"level":5,"x":25,"y1":1356.59046268884,"y2":2193.0315411135,"y3":2168.72189334818},{"series":3,"level":1,"x":1,"y1":35.8750566917037,"y2":36.056593539625,"y3":20.0753884258256},{"series":3,"level":2,"x":2.5,"y1":41.9121449459831,"y2":42.5654391343614,"y3":41.5527440508253},{"series":3,"level":3,"x":5,"y1":26.3124334021254,"y2":112.048198332547,"y3":60.674147803073},{"series":3,"level":4,"x":10,"y1":465.493882996188,"y2":544.831839610199,"y3":379.671322495027},{"series":3,"level":5,"x":25,"y1":1596.3890712337,"y2":1561.92899829512,"y3":1952.31440123854}]},"tolerance_limit":80,"acceptance_limit":50,"acceptance_absolute":false,"quantity_units":null,"rolling_data":false,"rolling_limit":3,"model_to_test":"Linear","generate_figure":false,"correction_allow":false,"correction_threshold":[0.9,1.1],"correction_forced_value":1,"correction_round_to":2,"optimizer_parameter":null,"significant_figure":4,"status":"done"}')
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

