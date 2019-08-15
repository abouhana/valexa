from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt

from valexa.ploting.ploters import PloterData
from valexa.ploting.encoders import PlotlyJSONEncoder
from valexa.ploting.utils import profile_to_dict
from valexa.ploting.plotly.canvas import ProfilePlotCanvas

from .forms import UploadFileForm
from .decorators import ajax_response

# Create your views here.

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(ajax_response(encoder=PlotlyJSONEncoder), name="post")
class ValexaView(FormView):

    def post(self, request, *args, **kwargs):
        data = PloterData(request.FILES["file"].file)
        # plots = [ProfilePlotCanvas(p) for p in data.profiles]
        return {
            "profiles": [profile_to_dict(p) for p in data.profiles],
        }
        

