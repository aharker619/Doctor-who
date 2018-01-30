# Timely and Effective Care Hospital Data
# Taken from: 
# https://data.medicare.gov/Hospital-Compare/Timely-and-Effective-Care-Hospital/yv7e-xc69
# Filters the dataframe for rows that have 'OP-20' 
# Used for creating prediction model for average wait times at hospitals


import pandas as pd


def data_OP_20 ():
	'''
	Filers dataframe for OP_20
	Returns dataframe with rows for OP_20 only
	'''

	df = pd.read_csv("Timely_and_Effective_Care_-_Hospital.csv")

	df = df.loc[df["Measure ID"] == "OP_20"]

	return df 
