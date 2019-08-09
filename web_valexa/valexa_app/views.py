from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView

from valexa.core.ploters import ProfilePloter, PloterData
from valexa.core.encoders import NumpyEncoder, PlotlyJSONEncoder

from .forms import UploadFileForm
from .decorators import ajax

# Create your views here.

@method_decorator(ajax(encoder=PlotlyJSONEncoder), name="post")
class ValexaView(FormView):

    template_name = "valexa_app/index.html"
    form_class = UploadFileForm

    def form_valid(self, form):
        data = PloterData(form.files["file"].file)
        return {"figures": ProfilePloter(data).figures,}

