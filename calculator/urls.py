from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.calculator, name="calculator"),
    url(r'^calculate/$', views.calculate, name="calculate"),
    url(r'^calculate-book/$', views.calculate_book, name="calculate-book"),
    url(r'^add/$', views.add_xero_to_list, name="add-xero-to-list"),
    url(r'^reset/$', views.reset_xero_list, name="add-xero-to-list"),
    url(r'^costs/(?P<costid>\d+)/delete/$', views.delete_cost, name="delete_cost")
]