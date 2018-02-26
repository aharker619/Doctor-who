from django.db import models
from django.db.models.expressions import RawSQL
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import math

# code from https://stackoverflow.com/questions/19703975/django-sort-by-distance/26219292#26219292
@receiver(connection_created)
def extend_sqlite(connection = None, **kwargs):
	if connection.vendor == "sqlite":
		cf = connection.connection.create_function
		cf('asin', 1, math.asin)
		cf('cos', 1, math.cos)
		cf('radians', 1, math.radians)
		cf('sin', 1, math.sin)
		cf('sqrt', 1, math.sqrt)
		cf('pow', 2, math.pow)


# reference https://stackoverflow.com/questions/19703975/django-sort-by-distance/26219292#26219292
# used haversine formula from Pa3
class LocationManager(models.Manager):
	def nearby(self, lat, lng, radius):
		'''
		Get queryset of locations within the given radius

		Inputs:
			lat: float, user latitude
			lng: float, user longitude
			radius: integer, radius around user in km
		'''
		haversine = """
					6367 * 2 * asin(sqrt(pow(sin((radians(%s) - radians(lat)) / 
					2), 2) + cos(radians(lat)) * cos(radians(%s)) * pow(sin((
					radians(%s) - radians(lng)) / 2), 2)))
					"""

		return self.get_queryset()\
				   .annotate(distance = RawSQL(haversine, (lat, lat, lng)))\
				   .filter(distance__lt = radius)\
				   .order_by('distance')


class EmergencyDept(models.Model):
	'''
	Database describing Emergency Departments
	
	Data gathered from Timely and Effective Hospital Data,
	Hospital General Information from Medicare's Hospital Compare,
	Census metro-micro delineation-files,
	state codes from https://github.com/jasonong/List-of-US-States/blob/master/states.csv,
	and zipcodes from http://federalgovernmentzipcodes.us/
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

	objects = LocationManager()
	# https://docs.djangoproject.com/en/2.0/topics/db/managers/
	# from_queryset see if you can set bounds this way

	def __str__(self):
		return self.name

	# https://stackoverflow.com/questions/7152497/making-a-python-user-defined-class-sortable-hashable
	def __lt__(self, other):
		if self.provider_id < other.provider_id:
			return True
		else:
			return False


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
	lng = models.FloatField()
	lat = models.FloatField()

	objects = LocationManager()
	
	def __str__(self):
		return self.name


class PatientWaittime(models.Model):
	'''
	Database describing patient wait times in select EDs
	
	Data gathered from NHAMCS 
	'''
	patient_id = models.IntegerField(primary_key = True)
	visit_month = models.IntegerField()
	visit_day = models.IntegerField()
	arrival_time = models.IntegerField()
	wait_time = models.IntegerField()
	immediacy = models.IntegerField()
	painscale = models.IntegerField()
	blinded_hospital_code = models.IntegerField()
	metro_area = models.FloatField(default = 0)
	year = models.IntegerField()

	def __repr__(self):
		return self.patient_id, self.wait_time


class ZipLocation(models.Model):
	'''
	Database connecting zipcodes to latitude and longitude locations
	Data from https://boutell.com/zipcodes/ with missing zipcodes filled in by
	ZCTA from Census https://www.census.gov/geo/maps-data/data/gazetteer2015.html
	See clean_zips.py 
	'''
	zipcode = models.CharField(primary_key = True, max_length = 9)
	lat = models.FloatField()
	lng = models.FloatField()

	def __str__(self):
		return self.zipcode
