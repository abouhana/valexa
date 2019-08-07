from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView

from valexa_app.decorators import ajax
from valexa_app.valexa.app import AppState, ValexaApp, NumpyEncoder

from .forms import UploadFileForm

# Create your views here.

@method_decorator(ajax(encoder=NumpyEncoder), name="post")
class ValexaView(FormView):

    template_name = "valexa_app/index.html"
    form_class = UploadFileForm

    def form_valid(self, form):
        app = ValexaApp(AppState())
        app.load_xlsx(form.files["file"].file)
        results = app.profiles_as_json()
        return {"results": results}

    def form_invalid(self, form):
        p=form
        return super().form_invalid()
