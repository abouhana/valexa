from valexa.examples.test_feinberg_uncertainty import test_feinberg_uncertainty
from valexa.examples.test_feinberg_coli import test_feinberg_coli
from valexa.examples.test_sfstp import test_sfstp
from valexa.examples.test_feinberg_labostat import test_feinberg_labostat
from valexa.examples.test_inra_pyrene import test_inra_pyrene
import json


def valexa_validate():
    number_of_pass = 0
    number_of_fail = 0

    validation_list = [
        {
            "name": "Feinberg, M., Labo-Stat (2010)",
            "function": test_feinberg_labostat,
            "index": 1,
            "tested_profile": 1,
        },
        {
            "name": "Feinberg et al., New advances in method validation and measurement uncertainty aimed at improving the quality of chemical data (2004)",
            "function": test_feinberg_uncertainty,
            "index": 2,
            "tested_profile": 1,
        },
        {
            "name": "Feinberg, M. et al., Validation of Alternative Methods for the Analysis of Drinking Water and Their Application to Escherichia coli (2011)",
            "function": test_feinberg_coli,
            "index": 3,
            "tested_profile": 3,
        },
        {
            "name": "Huyez-Levrat, M et al., Cahier technique de l'INRA - Validation des méthodes (2010)",
            "function": test_inra_pyrene,
            "index": 4,
            "tested_profile": 1,
        },
        {
            "name": "Hubert et al., Harmonization of strategies for the validation of quantitative analytical procedures. A SFSTP proposal - Part III (2004)",
            "function": test_sfstp,
            "index": 5,
            "tested_profile": 5,
        },
    ]

    print(
        json.dumps(
            {
                "type": "VALID_INFO",
                "data": {
                    "number_of_validation": len(validation_list),
                    "status": "start",
                    "number_of_pass": number_of_pass,
                    "number_of_fail": number_of_fail,
                },
            }
        )
    )

    for validation in validation_list:
        print(
            json.dumps(
                {
                    "type": "VALID_NAME",
                    "data": {
                        "validation_name": validation["name"],
                        "index": validation["index"],
                        "tested_profile": validation["tested_profile"],
                    },
                }
            )
        )
        try:
            validation["function"]()

        except AssertionError as error:
            number_of_fail += 1
            print(
                json.dumps(
                    {"type": "VALID_FAIL", "data": {"validation_fail": number_of_fail}}
                )
            )

        else:
            number_of_pass += 1
            print(
                json.dumps(
                    {"type": "VALID_PASS", "data": {"validation_pass": number_of_pass}}
                )
            )

    print(
        json.dumps(
            {
                "type": "VALID_INFO",
                "data": {
                    "number_of_validation": len(validation_list),
                    "status": "done",
                    "number_of_pass": number_of_pass,
                    "number_of_fail": number_of_fail,
                },
            }
        )
    )

    return True


if __name__ == "__main__":
    valexa_validate()
