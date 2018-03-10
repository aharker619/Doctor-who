# Alyssa Harker
# Original code except where specified
# Census data: 2015_Gaz_zcta_national.txt 
# source = https://www.census.gov/geo/maps-data/data/gazetteer2015.html
# zipcodes.csv source = https://boutell.com/zipcodes/

import pandas as pd


def clean_data():
    '''
    Get all zipcodes from zipcodes.csv and fill in any additional zipcodes from
    2015_Gaz_zcta_national.txt. The combination of these files covers all 
    zipcodes in the hospital database.
    
    Output:
        CSV with columns containing zipcode, latitude, and longitude values
    '''
    zcta = pd.read_table('2015_Gaz_zcta_national.txt', usecols = [0, 5, 6], 
                         dtype = {'GEOID': str})
    zcta.columns = ['zipcode', 'lat', 'lng']
    zips = pd.read_csv('zipcodes.csv', dtype = {'zip': str})
    zips = zips[['zip', 'latitude', 'longitude']].copy()
    
    # Modified Code: to get unique rows from two pandas dataframes
    #https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe
    df_all = zcta.merge(zips.drop_duplicates(), left_on = 'zipcode', right_on =
                        'zip', how = 'left', indicator = True)
    zcta_add = df_all[df_all['_merge'] == 'left_only'][['zipcode', 'lat', 
                                                        'lng']]
    # Original Code
    zcta_add.columns = ['zip', 'latitude', 'longitude']
    df = pd.concat((zips, zcta_add), axis = 0)

    df.to_csv('combined_zips.csv', index = False)