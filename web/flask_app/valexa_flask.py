from flask import Flask, jsonify, request
from flask_cors import CORS

from valexa.ploting.ploters import PloterData
from valexa.ploting.encoders import PlotlyJSONEncoder
from valexa.ploting.utils import profile_to_dict



# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.json_encoder = PlotlyJSONEncoder

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/valexa_app/compute/', methods=['POST'])
def compute():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = PloterData(request.files["file"].stream._file)
        response_object.update({
            "profiles": [profile_to_dict(p) for p in data.profiles],
        })
    
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()