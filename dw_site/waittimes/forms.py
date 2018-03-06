# Here is where you store form related classes

from django import forms

class UserForm(forms.Form):
	address = forms.CharField(max_length = 200)
	zipcode = forms.CharField(max_length = 5)
	user_pain = forms.ChoiceField(label = "Painscale (1-10)", choices = [("1", "1"), ("2", "2"), ("3", "3"),
	 ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), 
	 ("10", "10")])
	