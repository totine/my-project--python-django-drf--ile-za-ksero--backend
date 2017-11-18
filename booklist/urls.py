from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="index"),
    url(r'^books/(?P<bookid>\d+)$', views.book_details, name="book_details")
]