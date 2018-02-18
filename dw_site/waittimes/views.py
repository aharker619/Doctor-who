##https://docs.djangoproject.com/en/2.0/topics/forms/

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserForm

def user_info(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = UserForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data
			# this is where the calculations happen
			zipcode = form.cleaned_data['zipcode']
			# build helper functions in this view file?
			# redirect to new URL
			return HttpResponseRedirect('results/' + zipcode + '/')
	# if a GET or any other method, create a blank form
	# this is what happens the first time you visit the URL
	else:
		form = UserForm()
	return render(request, 'waittimes/user_info.html', {'form': form})



def results(request, zipcode):
	response = ("This is where the results are shown: {}".format(zipcode))
	return HttpResponse(response)

def index(request):
	return HttpResponse("This is the index page")