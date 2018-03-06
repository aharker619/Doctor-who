##https://docs.djangoproject.com/en/2.0/topics/forms/

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from waittimes.closest_hosp import find_closest, sort_hospitals
from waittimes.get_distance_duration import calculate_driving
from waittimes.get_weather_alerts import check_weather
import waittimes.regression as regression

from .forms import UserForm

def user_info(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
            address = form.cleaned_data['address']
            user_pain = form.cleaned_data['user_pain']
            # find closest hospitals, calculate driving time, predict waittime
            hosp_qs, uc_qs = find_closest(zipcode)
            hosp_qs = calculate_driving(address, zipcode, hosp_qs)
            # hosp_qs = run_regression(user_pain, hosp_qs)
            sort_hosp = sort_hospitals(hosp_qs)
            # check local weather
            weather = check_weather(zipcode)
            return render(request, 'waittimes/results.html', {'zipcode': 
                zipcode, 'sort_hosp': sort_hosp, 'uc_qs': uc_qs, 
                'weather':weather})
    # if a GET or any other method, create a blank form
    else:
        form = UserForm()
    return render(request, 'waittimes/user_info.html', {'form': form})


def results(request, zipcode, sort_hosp, uc_qs, weather):
    return render(request, 'waittimes/results.html', {'zipcode': zipcode, 'sort_hosp': sort_hosp, 
                  'uc_qs': uc_qs, 'weather': weather})


def uc_fyi(request):
    return render(request, 'waittimes/uc_fyi.html') 


def weather_alert(request, zipcode, weather):
    alerts_pre = weather.split("', ")
    alerts = [alert.strip("[]' ") for alert in alerts_pre]
    return render(request, 'waittimes/weather.html', {'zipcode': zipcode, 'weather': alerts})   


def index(request):
    return redirect('waittimes:user_info')
