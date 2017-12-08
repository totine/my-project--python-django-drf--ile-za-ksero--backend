from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'api/costs/$', views.CostListView.as_view()),
    url(r'api/costs/(?P<costid>\d+)$', views.CostDetails.as_view())
]