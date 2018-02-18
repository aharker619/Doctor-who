from uszipcode import ZipcodeSearchEngine
import pandas as pd 


def go():
	'''
	Find radius for searching closest hospitals
	Need to find maximum mile radius to find at least 5 
	ED from all zip codes. 
	For urgent care use 'urgent_care_data.csv' and 'ZIP'
	'''
	ed_data = pd.read_csv('HGI.csv', dtype = {'ZIP_Code': str})
	ed_data['ZIP_Code'] = ed_data['ZIP_Code'].apply(lambda x: x.zfill(5))
	uc_data = pd.read_csv('urgent_care_data.csv', dtype = {'ZIP': str})
	uc_data['ZIP'] = uc_data['ZIP'].apply(lambda x: x.zfill(5))
	codes = pd.read_csv('zipcode_us.csv', dtype = {'zipcode': str})
	codes['zipcode'] = codes['zipcode'].apply(lambda x: x.zfill(5))
	
	#combined = codes.merge(ed_data.drop_duplicates(), left_on = 'zipcode', 
		#right_on = zip_name, how = 'left', indicator = True)
	#check_zip = combined[combined['_merge'] == 'left_only'][['zipcode', 'state']] 
	check_zip = codes[(codes.state != 'PR') & (codes['zipcode type'] == 
		'Standard')].copy()
	already_checked = {}
	
	search = ZipcodeSearchEngine()
	print('finding closest')
	check_zip['closest'] = check_zip['zipcode'].apply(
		lambda x: zipcodes_one_radius(search, 500, x))
	print('finding hospitals')
	check_zip['hospitals'] = check_zip['closest'].apply(
		lambda x: find_all_hospitals(x, 'ZIP_Code', ed_data, 5))
	print('finding urgent cares')
	check_zip['urgent'] = check_zip['closest'].apply(
		lambda x: find_all_urgent(x, 'ZIP', uc_data, 1))
	
	return check_zip

def zipcodes_one_radius(search, miles, zipcode):
	'''
	get the 10 closest zipcodes from a given zipcode with radius miles
	'''
	my_zip = search.by_zipcode(zipcode)
	#print(my_zip, my_zip.Zipcode, my_zip.ZipcodeType)
	if my_zip.Zipcode:
		closest_10 = search.by_coordinate(my_zip.Latitude, my_zip.Longitude, 
			radius = miles, returns = 10)
		return closest_10
	else:
		return []
def find_all_hospitals(closest_10, zip_name, data, cutoff):
	all_hosp = pd.DataFrame()
	if closest_10:
		hosp_count = 0
		
		for zipcode in closest_10:
			hosp_df = find_hospitals(zipcode.Zipcode, zip_name, data)
			all_hosp = pd.concat((all_hosp, hosp_df))
			if all_hosp.shape[0] >= cutoff:
				break
	return all_hosp


def find_hospitals(zipcode, zip_name, data):
	'''
	Check if there is a hospital in a given zipcode
	'''
	local_hosp = data[data[zip_name] == zipcode]

	return local_hosp

