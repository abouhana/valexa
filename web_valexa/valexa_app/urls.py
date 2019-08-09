"""valexa app URL Configuration"""
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = "valexa_app"
urlpatterns = [
    path('compute/', views.ValexaView.as_view(), name="compute"),
    # path('compute/', TemplateView.as_view(template_name='valexa_app/index.html'), name="compute"),
]
