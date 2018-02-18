from django.urls import path

from . import views

urlpatterns = [
	path('user_info', views.user_info, name = 'user_info'),
	path('results/<int:zipcode>/', views.results, name = 'results'),
	path('', views.index, name = 'index'),
]