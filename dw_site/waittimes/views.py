##https://docs.djangoproject.com/en/2.0/topics/forms/

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from waittimes.closest_hosp import find_closest, sort_hospitals
from waittimes.get_distance_duration import calculate_driving

from .forms import UserForm

def user_info(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = UserForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# get current local time
			user_time = datetime.now()
			zipcode = form.cleaned_data['zipcode']
			address = form.cleaned_data['address']
			hosp_qs, uc_qs = find_closest(zipcode)
			hosp_qs = calculate_driving(address, zipcode, hosp_qs)
			#hosp_qs = predict_waittime(user_time, hosp_qs)
			sort_hosp = sort_hospitals(hosp_qs)
			# redirect to new URL
			# https://simpleisbetterthancomplex.com/tips/2016/05/05/django-tip-1-redirect.html
			return render(request, 'waittimes/results.html', {'zipcode': zipcode, 'sort_hosp': sort_hosp, 'uc_qs': uc_qs})
	# if a GET or any other method, create a blank form
	# this is what happens the first time you visit the URL
	else:
		form = UserForm()
	return render(request, 'waittimes/user_info.html', {'form': form})


def results(request, zipcode, sort_hosp, uc_qs):
	return render(request, 'results.html', {'zipcode': zipcode, 'sort_hosp': sort_hosp, 
				  'uc_qs': uc_qs})

def index(request):
	return HttpResponse("This is the index page")