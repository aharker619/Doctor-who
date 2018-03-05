from django.urls import path, re_path

from . import views

urlpatterns = [
	path('user_info', views.user_info, name = 'user_info'),
	path('results.html', views.results, name = 'results'),
	path('uc_fyi.html', views.uc_fyi),
	path('weather.html', views.weather_alert, name = 'weather_alert'),
	path('', views.index, name = 'index'),
]
