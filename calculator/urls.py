from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.calculator, name="calculator"),
    url(r'^calculate/$', views.calculate, name="calculate")
]