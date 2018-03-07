# Alyssa Harker
# 1/29/18
# update 2/13/18
# own code

import pandas as pd
import numpy as np

# The 2012 dataset does not include MSA data, so only use 2013-2015 to look at MSA
FILES = ['nhamcsed2015.csv', 'nhamcsed2014.csv', 'nhamcsed2013.csv', 'nhamcsed2012.csv']
COLUMNS = ['VMONTH', 'VDAYR', 'ARRTIME', 'WAITTIME', 'IMMEDR', 'PAINSCALE',
               'HOSPCODE', 'YEAR']
MSA_FILES = ['nhamcsed2015.csv', 'nhamcsed2014.csv', 'nhamcsed2013.csv']
MSA_COL = ['VMONTH', 'VDAYR', 'ARRTIME', 'WAITTIME', 'IMMEDR', 'PAINSCALE',
               'HOSPCODE', 'MSA', 'YEAR']

def load_data(filenames, columns, save = False, output_file = None):
    '''
    Loads data from filename and selects useful columns from NHAMCS survey
    Saves as csv with name output_file if save is True

    Inputs:
        filenames: list of tuples, year and filename for NHAMCS survey
        save: boolean, True if want to write as csv
        output_file, str, name of file to save data

    Output:
        returns data combined over all_years
        if save is True, also outputs csv file
    '''
    lower_cols = [x.lower() for x in columns]
    all_years = []
    for filename in filenames:

        if filename == 'nhamcsed2013.csv':
            data = pd.read_csv(filename, usecols = lower_cols)
            data.columns = columns
        else:
            data = pd.read_csv(filename, usecols = columns)

        wait_data = data[data.WAITTIME >= 0].copy()
        all_years.append(wait_data)
    all_years_df = pd.concat(all_years)
    
    if save:
        all_years_df.to_csv(output_file)

    return all_years_df