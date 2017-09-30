from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.calculator, name="calculator"),
    url(r'^calculate/$', views.calculate, name="calculate"),
    url(r'^calculate-book/$', views.calculate_book, name="calculate-book"),
    url(r'^by-weight/$', views.calculate_by_weight, name="calculate-by-weight"),
    url(r'^add/$', views.add_xero_to_list, name="add-xero-to-list"),
    url(r'^reset/$', views.reset_xero_list, name="add-xero-to-list"),
    url(r'^costs/(?P<costid>\d+)$', views.cost_view, name="cost_view"),
    url(r'^costs/(?P<costid>\d+)/delete/$', views.delete_cost, name="delete_cost"),
    url(r'^costs/(?P<costid>\d+)/edit/$', views.cost_edit, name="delete_cost"),
    url(r'^xerolists/(?P<xerolistid>\d+)$', views.xerolist_view, name="xerolist_view"),
    url(r'^xerolists/(?P<xerolistid>\d+)/delete$', views.xerolist_delete, name="xerolist_view")
]