import sys
import json
from valexa.electron_interface.boot_validation import valexa_validate
from valexa.electron_interface.ouput import output
from valexa.electron_interface.params_export import get_params
from warnings import filterwarnings

def main(arguments):

    if len(arguments) > 1:
        if arguments[1] == "validate":
            valexa_validate()

        if arguments[1] == "profile":
            ouptut(**json.loads(arguments[2]))

        if arguments[1] == "test":
            while(True):
                in_stream_data = input()
                parsed_stream_data = json.loads(in_stream_data)
                if parsed_stream_data == "EXIT":
                    break
                output(**parsed_stream_data)



        if arguments[1] == "get_params":
            get_params()

    print("EXIT")
    exit(0)


if __name__ == "__main__":
    filterwarnings("ignore")
    main(sys.argv)
