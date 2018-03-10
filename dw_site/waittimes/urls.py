# Alyssa Harker
# Modified Code: https://docs.djangoproject.com/en/2.0/intro/tutorial03/
# as well as TA input from Kartik Singhal further modified to support lists
# for 'weather_alert' url pattern

from django.urls import path, re_path

from . import views

app_name = 'waittimes'
urlpatterns = [
    path('user_info', views.user_info, name = 'user_info'),
    path('results.html', views.results, name = 'results'),
    path('uc_fyi.html', views.uc_fyi),
    re_path(r'^weather_alert/(?P<zipcode>\d+)/(?P<weather>.+)/$', 
                    views.weather_alert, name = 'weather_alert'),
    path('', views.index, name = 'index'),
]
