from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^api/chart/data/$', views.ChartData.as_view(), name='api-data'),
    path('search/', views.SearchView.as_view(), name="search"),
    path('signup/', views.handle_signup, name="signup"),
    path('login/', views.handle_login, name="login"),
    path('logout/', views.handle_logout, name="logout"),
    path('alert/', views.set_alert, name="alert"),
]

