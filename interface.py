import sys
import json
from valexa.electron_interface.boot_validation import valexa_validate
from valexa.electron_interface.dev_ouput import dev_ouptut
from valexa.electron_interface.params_export import get_params
from warnings import filterwarnings

def main(arguments):

    if len(arguments) > 1:
        if arguments[1] == "validate":
            valexa_validate()

        if arguments[1] == "test":
            dev_ouptut(json.loads(arguments[2]), None)

        if arguments[1] == "get_params":
            get_params()

    print("EXIT")
    exit(0)


if __name__ == "__main__":
    filterwarnings("ignore")
    main(sys.argv)
