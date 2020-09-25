from sys import argv, exit
from json import loads, dumps
from valexa.electron_interface.boot_validation import valexa_validate
from valexa.electron_interface.ouput import output
from valexa.electron_interface.params_export import get_params
from valexa.electron_interface.generateReport import generate
from warnings import filterwarnings

def main(arguments):

    if len(arguments) > 1:
        if arguments[1] == "validate":
            valexa_validate()

        if arguments[1] == "profile":
            output(**loads(arguments[2]))

        if arguments[1] == "test":
            dumps('READY')
            while(True):
                in_stream_data = input()
                if in_stream_data == '"EXIT"':
                    print("EXIT")
                    exit(0)

                parsed_stream_data = loads(in_stream_data)
                output(**parsed_stream_data)

        if arguments[1] == "get_params":
            get_params()

        if arguments[1] == "processProfilesReport":
            while(True):  # récupération du "data" de l'objet envoyé
                in_stream_data = input()
                if in_stream_data == '"EXIT"':
                    print("EXIT")
                    exit(0)
                parsed_stream_data = loads(in_stream_data)
                #parsed_stream_data = in_stream_data.strip('][').split(', ')  # convert into list

                print(dumps({"type": parsed_stream_data.__class__.__name__, "data": parsed_stream_data[1].__class__.__name__}))
                for profile in parsed_stream_data:
                    #p = loads(profile)
                    #print(dumps({"type": p.__class__.__name__, "data": p}))
                    generate(**profile)

                print(dumps({"type": "END", "data": in_stream_data}))

    print("EXIT")
    exit(0)


if __name__ == "__main__":
    filterwarnings("ignore")
    main(argv)
