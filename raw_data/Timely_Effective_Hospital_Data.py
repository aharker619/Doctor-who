# Timely and Effective Care Hospital Data
# Taken from: 
# https://data.medicare.gov/Hospital-Compare/Timely-and-Effective-Care-Hospital/yv7e-xc69
# Filters the dataframe for rows that have 'OP-20' 
# Used for creating prediction model for average wait times at hospitals


import pandas as pd


def data_OP_20():
	'''
	Filers dataframe for OP_20
	Returns dataframe with rows for OP_20 only
	'''

	df = pd.read_csv("Timely_and_Effective_Care_-_Hospital.csv", dtype = {'ZIP Code': str})

	df = df.loc[df["Measure ID"] == "OP_20"]
	
	#remove the white space in the column name with underscore
	df.columns = df.columns.str.replace('\s+', '_')

	df = df[['Provider_ID', 'Hospital_Name', 'Address', 'City', 'State', 'ZIP_Code', 
			 'County_Name', 'Phone_Number', 'Score', 'Sample']]

	# fill in missing zeros in zipcode
	df['ZIP_Code'] = df['ZIP_Code'].apply(lambda x: x.zfill(5))
	df.to_csv("time.csv", encoding='utf-8', index=False)
	
	return
