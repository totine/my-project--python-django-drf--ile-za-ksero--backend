from django.conf.urls import url

from booklist import views

urlpatterns = [
    url(r'^$', views.home)
]