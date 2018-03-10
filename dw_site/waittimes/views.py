# Alyssa Harker
# Modified and Original Code

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from waittimes.closest_hosp import find_closest, sort_hospitals
from waittimes.get_distance_duration import calculate_driving
from waittimes.get_weather_alerts import check_weather
import waittimes.regression as regression
import waittimes.prediction as prediction

from .forms import UserForm


model, x = prediction.find_model()


# Modified Code: https://docs.djangoproject.com/en/2.0/topics/forms/
def user_info(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = UserForm(request.POST)
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
            address = form.cleaned_data['address']
            user_pain = form.cleaned_data['user_pain']
            # find closest hospitals, calculate driving time, predict waittime
            hosp_qs, uc_qs = find_closest(zipcode)
            hosp_qs = calculate_driving(address, zipcode, hosp_qs)
            hosp_qs = prediction.run_regression(user_pain, hosp_qs, model, x)
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

# Modified Code: https://docs.djangoproject.com/en/2.0/intro/tutorial03/
def results(request, zipcode, sort_hosp, uc_qs, weather):
    return render(request, 'waittimes/results.html', {'zipcode': zipcode, 
                  'sort_hosp': sort_hosp, 'uc_qs': uc_qs, 'weather': weather})


def uc_fyi(request):
    return render(request, 'waittimes/uc_fyi.html') 


# Original Code for processesing weather variable
def weather_alert(request, zipcode, weather):
    alerts_pre = weather.split("', ")
    alerts = [alert.strip("[]' ") for alert in alerts_pre]
    alerts = [' '.join(alert.replace("\\n", " ").split('*')) for 
              alert in alerts]
    return render(request, 'waittimes/weather.html', {'zipcode': zipcode, 
                                                      'weather': alerts})


def index(request):
    return redirect('waittimes:user_info')
