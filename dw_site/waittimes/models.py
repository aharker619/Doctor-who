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
	condition = models.CharField(max_length = 30) # what is this?
	score = models.IntegerField()
	sample = models.IntegerField()
	location = models.CharField(max_length = 150)
	hospital_rating = models.IntegerField()

	def __unicode__(self):
		return self.name

class UrgentCare(models.Model):
	'''
	Database describing Urgent Care centers
	
	Data gathered from ArcGIS REST Services Directory
	'''
	provider_id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 150)
	address = models.CharField(max_length = 100)
	address_2 = models.CharField(max_length = 100)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 2)
	zipcode = models.CharField(max_length = 9)
	phone_number = models.CharField(max_length = 12)
	latitude = models.FloatField()
	longitude = models.FloatField()

	def __unicode__(self):
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
	metro_area = models.IntegerField()
	year = models.IntegerField()

	def __unicode__(self):
		return self.wait_time


class User(models.Model):
	zipcode = models.CharField(max_length = 9)
	# need this for day, month, and time
	user_time = models.TimeField()
	user_date = models.DateField()

	def get_closest_zipcodes(self):
		'''
		Calculate latitude and longitude of User
		Calculate closest 10 zip codes?
		'''
		search = ZipcodeSearchEngine()
		user_loc = search.by_zipcode(self.zipcode)

		closest_10_zip = search.by_coordinate(user_loc.Latitude, 
			user_loc.Longitude, radius = 50, returns = 10)

		return closest_10_zip
	closest_10_zip = property(get_closest_zipcodes)

	def __unicode__(self):
		return self.zipcode

# are classes needed for APIs?

# Thoughts: we could have a database already populated with closest hospitals
# also urgent cares
# zipcode look up would find closest hospitals to do driving calc, and urgent care
# saves using zipcodesearch within website
# can you create a database built from already established databases?
'''
class ZipcodeLink(models.Model):
'''
'''
	user_zip = models.CharField(max_length = 9)
	closest_eds = models.ForeignKey(EmergencyDept, on_delete = models.CASCADE)
	closest_uc = models.ForeignKey(UrgentCare, on_delete = models.CASCADE)
'''
#class Weather(models.Model):


#class Maps(models.Model):

