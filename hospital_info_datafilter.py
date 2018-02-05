# Tianchu Shu
import pandas as pd
import csv

df = pd.read_csv("Hospital_General_Information.csv")

#remove the white space in the column name with underscore
df.columns = df.columns.str.replace('\s+', '_')

#filter the hospitals with emergency room
df_ER = df[df["Emergency_Services"] == True]

selcon  = ['Provider_ID', 'ZIP_Code','Hospital_overall_rating']

df_ER = df_ER[selcon]

df_ER.to_csv("HGI.csv", encoding='utf-8', index=False)
