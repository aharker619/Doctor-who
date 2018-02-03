# Alyssa Harker
# 1/29/18
# own code

import pandas as pd
import numpy as np

FILENAME = 'nhamcsed2015.csv'
def load_data(FILENAME, save = False):
    '''
    Loads data from filename and selects useful columns from NHAMCS survey
    Saves as csv if save is True

    Inputs:
    	FILENAME: str, filename for NHAMCS survey
    	save: boolean, True if want to write as csv
    '''
    columns = ['VMONTH', 'VDAYR', 'ARRTIME', 'WAITTIME', 'IMMEDR', 'PAINSCALE',
               'HOSPCODE', 'AMBDIV', 'TOTHRDIVR', 'PHYSPRACTRIA', 'FASTTRAK', 
               'REGION', 'MSA']

    nhamcs_data = pd.read_csv(FILENAME, usecols = columns)
    if save:
    	nhamcs_data.to_csv('nhamcs_data.csv')
    return nhamcs_data