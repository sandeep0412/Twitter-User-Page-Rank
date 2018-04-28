from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^input', views.InputPageView.as_view(), name='input'),
    url(r'^output', views.OutputPageView.as_view(), name='output')
]