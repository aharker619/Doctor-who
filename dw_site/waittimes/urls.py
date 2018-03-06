from django.urls import path, include

from . import views

app_name = 'waittimes'
urlpatterns = [
    path('user_info', views.user_info, name = 'user_info'),
    path('results.html', views.results, name = 'results'),
    path('uc_fyi.html', views.uc_fyi),
    path('weather_alert', views.weather_alert, name = 'weather_alert'),
    path('', views.index, name = 'index'),
]
