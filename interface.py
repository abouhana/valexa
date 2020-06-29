import sys
from valexa.electron_interface.boot_validation import valexa_validate
from warnings import filterwarnings

def main(arguments):

    if len(arguments) > 1:
        if arguments[1] == "validate":
            valexa_validate()

    print("EXIT")
    exit(0)


if __name__ == '__main__':
    filterwarnings("ignore")
    main(sys.argv)