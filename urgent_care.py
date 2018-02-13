# Alyssa Harker
# 2/13/18
# own code

import pandas as pd

def load_uc_data(save = False, output_file = ''):
	'''
	Load urgent care data and save as csv if save = True with name output_file
	'''
	filename = 'Urgent_Care_Facilities.csv'
	cols = ['ID', 'NAME', 'TELEPHONE', 'ADDRESS', 'ADDRESS2', 'CITY', 'STATE',
			'ZIP', 'X', 'Y']
	rename_cols = cols[1:8] + ['LONG', 'LAT']

	uc_data = pd.read_csv(filename, usecols = cols, index_col = 'ID')
	uc_data.columns = rename_cols
	if save:
		uc_data.to_csv(output_file)
	
	return uc_data


	