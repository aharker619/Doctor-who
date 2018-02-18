# should we do this using SQLite or use the databases themselves through django?

import sqlite3
import os
from uszipcode import ZipcodeSearchEngine
from math import radians, cos, sin, asin, sqrt

# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'waittime_info.sqlite3')


def find_closest(zipcode):
	'''
	Given a zipcode from ui, return the 5 closest hospitals and closest urgent care
	Input:
		zipcode: str
	Output:
		tuple: (query for hospitals, query for urgent care)
	'''
	if not args_from_ui:
        return ([], [])

    # convert zipcode to lat/long
    search = ZipcodeSearchEngine()
    my_zip = search.by_zipcode(zipcode)
    lat = my_zip.Latitude
    lng = my_zip.Longitude

   	# build query for hospitals
   	hosp_query = get_closest_hosp(lat, lng, 5, 'ed')
   	# get table
   	hospitals = run_query(hosp_query)

   	# build query for urgent care
   	uc_query = get_closest_hosp(lat, lng, 1, 'uc')
   	# get table
   	urgentcare = run_query(uc_query)

   	return (hospitals, urgentcare)

def get_closest_hosp(lat, lng, limits, data):
	'''
	'''
	query = 'SELECT'

def run_query(query):
    '''
    Opens connection to database in sqlite3 and returns results
    Inputs:
        query: str, sqlite3 query for closest hospitals
    Outputs:
        results: list, list of tuples of table results of query
    '''
    # connect to database and get cursor object
    conn = sqlite3.connect(DATABASE_FILENAME)
    c = conn.cursor()
    # only load function if walking time is needed
    conn.create_function("dist_between", 4, haversine)
    r = c.execute(query, param_tup)
    # get all results from table and get clean headers for attributes
    results = r.fetchall()
    conn.close()
    
    return results



def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the circle distance between two points
    on the earth (specified in decimal degrees)
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    m = km * 1000
    return km
