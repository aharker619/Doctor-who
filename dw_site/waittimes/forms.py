# Alyssa Harker
# Modified Code: Forms: https://docs.djangoproject.com/en/2.0/ref/forms/api/#django.forms.Form
# Validation Error: https://docs.djangoproject.com/en/2.0/ref/forms/validation/#raising-validation-error


from django.core.exceptions import ObjectDoesNotExist
from waittimes.models import ZipLocation
from django import forms


class UserForm(forms.Form):
    address = forms.CharField(max_length = 200)
    zipcode = forms.CharField(max_length = 5)
    user_pain = forms.ChoiceField(label = "Painscale (1-10)", choices = 
                [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
                 ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")])


    def clean_zipcode(self):
        '''
        During validation, check weather zipcode in data is within the 
        ZipLocation database. If not, raise a ValidationError.
        '''
        data = self.cleaned_data['zipcode']
        try:
            my_zip = ZipLocation.objects.get(zipcode = data)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Please enter a valid zipcode.")
        return data
    