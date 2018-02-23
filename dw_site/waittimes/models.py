from django.db import models
from uszipcode import ZipcodeSearchEngine

class EmergencyDept(models.Model):
	'''
	Database describing Emergency Departments
	
	Data gathered from Timely and Effective Hospital Data and
	Hospital General Information from Medicare's Hospital Compare
	'''
	provider_id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 150)
	address = models.CharField(max_length = 150)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 2)
	zipcode = models.CharField(max_length = 9)
	phone_number = models.CharField(max_length = 12)
	score = models.IntegerField()
	sample = models.IntegerField()
	hospital_rating = models.IntegerField()
	lng = models.FloatField(default = 0)
	lat = models.FloatField(default = 0)
	msa = models.CharField(max_length = 20, default = '')
	driving_time = models.FloatField(default = 0)
	predicted_wait = models.FloatField(default = 0) 

	def __str__(self):
		return self.name

class UrgentCare(models.Model):
	'''
	Database describing Urgent Care centers
	
	Data gathered from ArcGIS REST Services Directory
	'''
	provider_id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 150)
	telephone = models.CharField(max_length = 12)
	address = models.CharField(max_length = 100)
	address2 = models.CharField(max_length = 100)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 2)
	zipcode = models.CharField(max_length = 9)
	lng = models.FloatField(default = 0)
	lat = models.FloatField(default = 0)
	
	def __str__(self):
		return self.name


class PatientWaittime(models.Model):
	'''
	Database describing patient wait times in select EDs
	
	Data gathered from NHAMCS 
	'''
	patient_id = models.IntegerField(primary_key = True)
	# change to DateTimeField if better
	visit_month = models.IntegerField()
	visit_day = models.IntegerField()
	arrival_time = models.IntegerField()
	wait_time = models.IntegerField()
	immediacy = models.IntegerField()
	painscale = models.IntegerField()
	blinded_hospital_code = models.IntegerField()
	metro_area = models.FloatField(default = 0)
	year = models.IntegerField()

	def __unicode__(self):
		return self.patient_id, self.wait_time



