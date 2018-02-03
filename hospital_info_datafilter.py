import pandas as pd
import numpy as np
import csv

df = pd.read_csv("Hospital_General_Information.csv")

df_ER = df[df["Emergency Services"] == True]
#filter the hospitals with emergency room
