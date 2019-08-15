"""valexa app URL Configuration"""
from django.urls import include, path

from . import views

app_name = "valexa_app"
urlpatterns = [
    path('compute/', views.ValexaView.as_view(), name="compute"),
]
