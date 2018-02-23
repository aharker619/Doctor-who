# Here is where you store form related classes

from django import forms

class UserForm(forms.Form):
	address = forms.CharField(max_length = 200)
	zipcode = forms.CharField(max_length = 9)