# need to convert csv data to json
# to load into django dataframes

import pandas as pd
import json

def get_json_hosp(datafile, zip_name, id_name, model, output_file):
	'''
	'''
	data = pd.read_csv(datafile, dtype = {id_name:int, zip_name: str})
	data[zip_name] = data[zip_name].apply(lambda x: x.zfill(5))
	# make columns same as model attributes
	if model == 'EmergenyDept':
		cols = ['provider_id', 'name', 'address', 'city', 'state'
		'zipcode', 'phone_number', 'condition', 'score', 'sample', 'location'
		'hospital_rating']
	elif model == 'UrgentCare':
		cols = ['provider_id', 'name', 'address', 'address_2', 'city', 
		'state', 'zipcode', 'phone_number', 'latitude', 'longitude']
	data.columns = cols
	data['model'] = 'waittimes.' + model

	# https://stackoverflow.com/questions/40470954/convert-pandas-dataframe-to-nested-json
	j = (data.groupby(['model', 'provider_id'], as_index = False).apply(
		lambda x: x[cols[0:-1]].to_dict("r")).reset_index().rename(
		columns = {0: 'fields', 'provider_id':'pv'}).to_json(orient = 'records'))

	with open(output_file, 'w') as outfile:
		json.dump(j, outfile)
	
	return j

def get_json_patient(output_file):
	nhamcs_msa_data = pd.read_csv('nhamcs_msa_years.csv')
	nhamcs_all = pd.read_csv('nhamcs_all_years.csv')

	n12 = nhamcs_all[nhamcs_all.year == '2012']
	data = pd.concat((nhamcs_msa_data, n12), axis = 0)

	cols = ['patient_id', 'visit_month', 'visit_day', 'arrival_time', 'wait_time'
	'immediacy', 'painscale', 'blinded_hospital_code', 'metro_area', 'year']

	data.columns = cols
	data['model'] = 'waittimes.PatientWaittime'

	j = (data.groupby(['model', 'patient_id'], as_index = False).apply(
		lambda x: x[cols[0:-1]].to_dict("r")).reset_index().rename(
		columns = {0: 'fields', 'provider_id':'pv'}).to_json(orient = 'records'))

	with open(output_file, 'w') as outfile:
		json.dump(j, outfile)
	
	return j