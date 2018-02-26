# clean up 2015_Gaz_zcta_national.txt and fill in missing zipcodes in zipcodes.csv
# data from Census https://www.census.gov/geo/maps-data/data/gazetteer2015.html
# https://boutell.com/zipcodes/ for zipcodes.csv
import pandas as pd

def clean_data():
	'''
	Get zipcode, latitude, and longitude files from 2015_Gaz_zcta_national.txt
	Save as csv
	'''
	zcta = pd.read_table('2015_Gaz_zcta_national.txt', usecols = [0, 5, 6], dtype = {'GEOID': str})
	zcta.columns = ['zipcode', 'lat', 'lng']

	zips = pd.read_csv('zipcodes.csv', dtype = {'zip': str})
	zips = zips[['zip', 'latitude', 'longitude']].copy()
	#https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe
	df_all = zcta.merge(zips.drop_duplicates(), left_on = 'zipcode', right_on = 'zip', how = 'left', indicator = True)
	zcta_add = df_all[df_all['_merge'] == 'left_only'][['zipcode', 'lat', 'lng']]
	zcta_add.columns = ['zip', 'latitude', 'longitude']
	df = pd.concat((zips, zcta_add), axis = 0)

	df.to_csv('combined_zips.csv', index = False)
