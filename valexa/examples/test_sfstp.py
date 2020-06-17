from valexa.profiles import ProfileManager
from valexa.examples.dataset import sample_dataset

import pandas as pd
import numpy as np


def test_sfstp():
    """
    Dataset from:
    Hubert et al., Harmonization of strategies for the validation of quantitative analytical procedures. A SFSTP proposal - Part III

    This dataset is taken from the original proposal and is probably one of the most complete. It contains the data for
    the following regression models:
    - Linear through 0
    - Linear through 0 with partial dataset (up to Calibration level 4)
    - Linear
    - Weighted linear 1/X
    - log(X) - log(Y) (not available in Valexa at the moment)
    - sqrt(X) - sqrt(Y) (not available in Valexa at the moment)
    - Quadratic
    - Weighted quadratic 1/X

    The reference DataFrame is as follow:

     Level | repeatability_std | inter_series_std | tolerance_std | bias  | abs_tolerance_low | abs_tolerance_high
    -------+-------------------+------------------+---------------+-------+-------------------+--------------------
      1    | 0.141             | 0.092            | 0.173         | 0.024 | -0.206            | 0.254
    -------+-------------------+------------------+---------------+-------+-------------------+--------------------
      2    | 0.093             | 0.081            | 0.127         | 0.055 | -0.115            | 0.225
    -------+-------------------+------------------+---------------+-------+-------------------+--------------------
      3    | 0.099             | 0.141            | 0.178         | 0.093 | -0.147            | 0.333

    The reference DataFrame for the model is as follow (only Serie 1 is checked):

     Model                    | X        | Origin   | X^2
    --------------------------+----------+----------+----------------
     Linear through 0         | 0.002478 | 0        | 0
    --------------------------+----------+----------+----------------
     Linear through 0 partial | 0.002514 | 0        |
    --------------------------+----------+----------+----------------
     Linear                   | 0.002510 | -0.01932 |
    --------------------------+----------+----------+----------------
     1/X Weighted Linear     | 0.002523 | -0.02305 |
    --------------------------+----------+----------+----------------
     Quadratic                | 0.002656 | -0.02289 | -0.0000001480
    --------------------------+----------+----------+----------------
     1/X Weighted Quadratic   | 0.002570 | -0.02531 | -0.00000006084

    Note: There is a ~0.1% disrepancy in the Linear models that pass through 0. This is still under investigation.
    """
    data = sample_dataset.dataset("sfstp")

    profiles: ProfileManager = ProfileManager(
        "Test",
        data,
        acceptance_limit=20,
        tolerance_limit=90,
        #model_to_test=["Linear through 0", "Linear", "1/X Weighted Linear", "Quadratic", "1/X Weighted Quadratic"],
        model_to_test=["Linear"],
        rolling_data_limit=4,
        rolling_data=False
    )
    profiles.make_profiles()

    litterature_model_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "Slope": {
                1: 70.986,
                2: 69.875,
                3: 69.167
            },
            "Origin": {
                1: -5.494,
                2: -5.100,
                3: -5.767
            }
        }
    )
    litterature_dataframe: pd.DataFrame = pd.DataFrame(
        {
            "repeatability_std": {
                1: 0.0058,
                2: 0.0296,
                3: 0.0816
            },
            "inter_series_std": {
                1: 0.0153,
                2: 0.0442,
                3: 0.0281
            },
            "tolerance_std": {
                1: 0.0187,
                2: 0.0598,
                3: 0.0919
            },
            "bias": {
                1: 2.3,
                2: 0.5,
                3: -1.1
            },
            "abs_tolerance_low": {
                1: -0.206,
                2: -0.115,
                3: -0.147
            },
            "abs_tolerance_high": {
                1: 0.254,
                2: 0.225,
                3: 0.333
            },
        })

    #assertion_dataframe: pd.DataFrame = profiles.profiles["Direct"][0].get_profile_parameter(["repeatability_std",
    #                                                                                          "inter_series_std",
    #                                                                                          "tolerance_std",
    #                                                                                          "bias"]).round(3)

    #assertion_dataframe[["abs_tolerance_low", "abs_tolerance_high"]] = pd.DataFrame(
    #    profiles.profiles["Direct"][0].get_profile_parameter(["abs_tolerance"]).abs_tolerance.tolist(),
    #    index=assertion_dataframe.index
    #).round(3)



    reg_params_dict: dict = {
        "Model": [],
        "Series": [],
        "Intercept": [],
        "Slope": [],
        "Quad. term.": [],
        "Weighting factor": [],
        "r²": [],
        "Residual d.f.": []
    }

    true_prec_dict: dict = {
        "Model": [],
        "Introduced concentration (ng/ml)": [],
        "Mean calculated concentration (ng/ml)": [],
        "Bias (ng/ml)": [],
        "Relative bias (%)": [],
        "Recovery (%)": [],
        "Repeatability standard deviation (ng/ml)": [],
        "Between series standard deviation (ng/ml)": [],
        "Intermediate precision standard deviation (ng/ml)": [],
        "CV repeatability (%)": [],
        "CV intermediate precision (%)": []
    }

    p_t_te_me_dict: dict = {
        "Model": [],
        "Concentration (ng/ml)": [],
        "Intermediate precision (ng/ml)": [],
        "Trueness (ng/ml)": [],
        "Absolute total error (ng/ml)": [],
        "Relative total error (%)": [],
        "Maximal observed error (%)": []
    }

    calc_x_dataframe: pd.DataFrame = profiles.data_objects[0].validation_data[["Serie", "Level", "x"]]
    rel_acc_dataframe: pd.DataFrame = profiles.data_objects[0].validation_data[["Serie", "Level", "x"]]


    for key, value in profiles.profiles.items():
        calc_x_dataframe[key] = np.array([np.format_float_positional(np.float32(num), precision=4, trim="0", fractional=False) for num in value[0].model.data_x_calc])
        rel_acc_dataframe[key] = ((value[0].model.validation_data["x_calc"] - value[0].model.validation_data["x"])/value[0].model.validation_data["x"]*100).astype(float).round(2)

        for serie, serie_value in value[0].model.fit.items():
            reg_params_dict["Model"].append(key)
            reg_params_dict["Series"].append("Serie " + str(serie))
            if "Intercept" in serie_value.params:
                reg_params_dict["Intercept"].append(np.format_float_scientific(serie_value.params["Intercept"], precision=3))
            else:
                reg_params_dict["Intercept"].append("-")
            reg_params_dict["Slope"].append(np.format_float_scientific(serie_value.params["x"], precision=3))
            if "I(x ** 2)" in serie_value.params:
                reg_params_dict["Quad. term."].append(np.format_float_scientific(serie_value.params["I(x ** 2)"], precision=3))
            else:
                reg_params_dict["Quad. term."].append("-")
            reg_params_dict["Weighting factor"].append(value[0].model.weight)
            reg_params_dict["r²"].append(serie_value.rsquared.round(4))
            reg_params_dict["Residual d.f."].append(int(serie_value.df_resid))

        for level, level_value in value[0].profile_levels.items():

            true_prec_dict["Model"].append(key)
            true_prec_dict["Introduced concentration (ng/ml)"].append(level_value.introduced_concentration)
            true_prec_dict["Mean calculated concentration (ng/ml)"].append(level_value.calculated_concentration)
            true_prec_dict["Bias (ng/ml)"].append(level_value.bias)
            true_prec_dict["Relative bias (%)"].append(level_value.relative_bias)
            true_prec_dict["Recovery (%)"].append(level_value.recovery)
            true_prec_dict["Repeatability standard deviation (ng/ml)"].append(level_value.repeatability_std)
            true_prec_dict["Between series standard deviation (ng/ml)"].append(level_value.inter_series_std)
            true_prec_dict["Intermediate precision standard deviation (ng/ml)"].append(level_value.intermediate_precision_std)
            true_prec_dict["CV repeatability (%)"].append(level_value.repeatability_cv)
            true_prec_dict["CV intermediate precision (%)"].append(level_value.intermediate_precision_cv)

            p_t_te_me_dict["Model"].append(key)
            p_t_te_me_dict["Concentration (ng/ml)"].append(level_value.introduced_concentration)
            p_t_te_me_dict["Intermediate precision (ng/ml)"].append(round(level_value.intermediate_precision_std, 2))
            p_t_te_me_dict["Trueness (ng/ml)"].append(round(level_value.bias, 3))
            p_t_te_me_dict["Absolute total error (ng/ml)"].append(round(level_value.total_error_abs, 3))
            p_t_te_me_dict["Relative total error (%)"].append(round(level_value.total_error_rel, 3))
            p_t_te_me_dict["Maximal observed error (%)"].append("-")


    reg_params_dataframe: pd.DataFrame = pd.DataFrame(reg_params_dict)
    true_prec_dataframe: pd.DataFrame = pd.DataFrame(true_prec_dict)
    p_t_te_me_dataframe: pd.DataFrame = pd.DataFrame(p_t_te_me_dict)

    assert assertion_dataframe.equals(litterature_dataframe)