# Alyssa Harker
# Original and Modified Code specified below

from django.db import models
from django.db.models.expressions import RawSQL
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import math


# Modified Code: https://stackoverflow.com/questions/19703975/django-sort-by-distance/26219292#26219292
# modified equations needed for haversine
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


# Modifed Code: source of Custom Query Set used as_manager:
# https://simpleisbetterthancomplex.com/tips/2016/08/16/django-tip-11-custom-manager-with-chainable-querysets.html    
class LocationQuerySet(models.QuerySet):
    def rough_filter(self, lat, lng):
        '''
        Get queryset of locations within bounding box of 5 degrees latitude 
        and 6 degrees longitude.

        Inputs:
            self: model instances to query
            lat: float, user latitude
            lng: float, user longitude
        '''
        lat1 = lat - 5
        lat2 = lat + 5
        lng1 = lng - 6
        lng2 = lng + 6
        
        return self.filter(lat__range =  (lat1, lat2), 
                                          lng__range = (lng1, lng2))


    # Modified Code: combined haversine formula from CS122 Pa3 with 
    # https://stackoverflow.com/questions/19703975/django-sort-by-distance/26219292#26219292
    def nearby(self, lat, lng, radius):
        '''
        Get queryset of locations within the given radius

        Inputs:
            self: model instances to query
            lat: float, user latitude
            lng: float, user longitude
            radius: integer, radius around user in km
        '''
        haversine = """
                    6367 * 2 * asin(sqrt(pow(sin((radians(%s) - radians(lat)) / 
                    2), 2) + cos(radians(lat)) * cos(radians(%s)) * pow(sin((
                    radians(%s) - radians(lng)) / 2), 2)))
                    """

        return self.annotate(distance = RawSQL(haversine, (lat, lat, lng)))\
                   .filter(distance__lt = radius)\
                   .order_by('distance')


# Orignial Code: https://docs.djangoproject.com/en/2.0/intro/tutorial02/#creating-models
class EmergencyDept(models.Model):
    '''
    Database describing Emergency Departments
    
    Data gathered from Timely and Effective Hospital Data,
    Hospital General Information from Medicare's Hospital Compare,
    Census metro-micro delineation-files,
    state codes from https://github.com/jasonong/List-of-US-States/blob/master/states.csv,
    and zipcodes from https://www.census.gov/geo/maps-data/data/gazetteer2015.html
    and https://boutell.com/zipcodes/

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
    predicted_wait = models.CharField(max_length = 20, default = '') 

    objects = LocationQuerySet().as_manager()

    def __str__(self):
        return self.name

    # Modified Code:
    # https://stackoverflow.com/questions/7152497/making-a-python-user-defined-class-sortable-hashable
    def __lt__(self, other):
        if self.provider_id < other.provider_id:
            return True
        else:
            return False


# Original Code: https://docs.djangoproject.com/en/2.0/intro/tutorial02/#creating-models
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

    objects = LocationQuerySet().as_manager()
    
    def __str__(self):
        return self.name


class ZipLocation(models.Model):
    '''
    Database connecting zipcodes to latitude and longitude locations

    Data from https://boutell.com/zipcodes/ with missing zipcodes filled in by
    ZCTA from https://www.census.gov/geo/maps-data/data/gazetteer2015.html 
    '''
    zipcode = models.CharField(primary_key = True, max_length = 9)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.zipcode
