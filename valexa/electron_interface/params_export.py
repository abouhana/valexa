from docstring_parser import parse
from valexa.profiles import ProfileManager
from valexa.models import ModelsManager
from json import dumps


def get_params():
    parameters = parse(ProfileManager.__init__.__doc__)

    parameters_list = [{
        'parameter': param.arg_name,
        'description': param.description,
        'default': param.default,
        'optional': param.is_optional,
        'type': param.type_name
    } for param in parameters.params]

    print(dumps({'type': 'PARAMS_LIST', 'data': parameters_list}).replace(': "None"', ': "null"'))
    print(dumps({'type': 'MODEL_LIST', 'data': ModelsManager.get_available_models()}))
    print(dumps({'type': 'DONE'}))