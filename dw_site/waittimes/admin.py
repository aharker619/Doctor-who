# Alyssa Harker
# Modified: Django generated, 
# https://docs.djangoproject.com/en/2.0/intro/tutorial02/#introducing-the-django-admin

from django.contrib import admin
from .models import EmergencyDept, UrgentCare, ZipLocation

admin.site.register(EmergencyDept)
admin.site.register(UrgentCare)
admin.site.register(ZipLocation)
