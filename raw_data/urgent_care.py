# Alyssa Harker
# 2/13/18
# own code
# data from https://hifld-dhs-gii.opendata.arcgis.com/datasets/0d748999f5eb4e76a7e0389442381af6_0?geometry=-30.27%2C-0.777%2C166.253%2C71.723

import pandas as pd

def load_uc_data(save = False, output_file = ''):
    '''
    Load urgent care data and save as csv if save = True with name output_file
    '''
    filename = 'Urgent_Care_Facilities.csv'
    cols = ['ID', 'NAME', 'TELEPHONE', 'ADDRESS', 'ADDRESS2', 'CITY', 'STATE',
            'ZIP', 'X', 'Y']
    rename_cols = cols[1:8] + ['LNG', 'LAT']
    lower_cols = [i.lower() for i in rename_cols]
    
    uc_data = pd.read_csv(filename, usecols = cols, dtype = {'ZIP': str}, 
                          index_col = 'ID')
    uc_data.columns = lower_cols
    uc_data['zip'] = uc_data['zip'].apply(lambda x: x.zfill(5))

    if save:
        uc_data.to_csv(output_file, sep = '|')
    
    return uc_data


    
