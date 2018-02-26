from django.contrib import admin

# Register your models here.
from .models import EmergencyDept, UrgentCare, PatientWaittime, ZipLocation

admin.site.register(EmergencyDept)
admin.site.register(UrgentCare)
admin.site.register(PatientWaittime)
admin.site.register(ZipLocation)
