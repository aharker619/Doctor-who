# Tianchu Shu
# Hospital General Information from Medicare Hospital Compare
import pandas as pd
import csv
from uszipcode import ZipcodeSearchEngine


def go():
	'''
	Read in Hospital_General_Information.csv
	Calculate latitude and longitude off of zipcode column
	Determine if hospital is MSA from msa.csv
	Save a csv file with given columns
	'''
	df = pd.read_csv("Hospital_General_Information.csv")

	#remove the white space in the column name with underscore
	df.columns = df.columns.str.replace('\s+', '_')

	#filter the hospitals with emergency room
	df_ER = df[df["Emergency_Services"] == True]

	selcon  = ['Provider_ID', 'ZIP_Code', 'Hospital_overall_rating']

	df_ER = df_ER[selcon]

	df_ER.to_csv("HGI.csv", encoding='utf-8', index=False)

