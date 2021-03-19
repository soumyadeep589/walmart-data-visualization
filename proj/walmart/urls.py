from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^api/chart/data/$', views.ChartData.as_view(), name='api-data'),
    path('search/', views.SearchView.as_view(), name="search"),
]

