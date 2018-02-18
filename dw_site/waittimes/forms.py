# Here is where you store form related classes

from django import forms
from waittimes.models import User
'''
class UserForm(forms.ModelForm):
	zipcode = forms.CharField(max_length = 9)
	user_time = forms.DateTimeField()
	user_date = forms.DateTimeField()
'''
# don't know if ModelForm is necessary or just Form. Could do without the model?
# technically don't need to store the user data past processing
class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['zipcode', 'user_time', 'user_date']