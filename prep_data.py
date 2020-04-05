import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime


df = pd.read_csv('./result/covid19_thai_province_timeline.csv')
df = df.iloc[:,1:]
df['Growth'] = df.apply(lambda x: x['NewCases']/x['TotalConfirmCases'] if x['TotalConfirmCases'] > 9 else 0, axis=1)
df_first_case = df[df['TotalConfirmCases']>0].drop_duplicates(['ProvinceId'], keep='first')
df_first_case.columns = ['ProvinceId', 'Province', 'ProvinceEn', 'First_Case_Date', 'First_Case_NewCases', 'First_Case_TotalConfirmCases', 'First_Case_Growth']

idx = df.groupby(['ProvinceId'])['Growth'].transform(max) == df['Growth']
df_max_growth = df[idx].drop_duplicates(['ProvinceId'], keep='first')
df_max_growth.columns = ['ProvinceId', 'Province', 'ProvinceEn', 'Max_Growth_Date', 'Max_Growth_NewCases', 'Max_Growth_TotalConfirmCases', 'Max_Growth_Growth']

idx = df.groupby(['ProvinceId'])['NewCases'].transform(max) == df['NewCases']
df_max_new = df[idx].drop_duplicates(['ProvinceId'], keep='first')
df_max_new.columns = ['ProvinceId', 'Province', 'ProvinceEn', 'Max_New_Date', 'Max_New_NewCases', 'Max_New_TotalConfirmCases', 'Max_New_Growth']

# merge
df_date = df_first_case.merge(df_max_growth, left_on=['ProvinceId', 'Province', 'ProvinceEn'], right_on=['ProvinceId', 'Province', 'ProvinceEn'])
df_date = df_date.merge(df_max_new, left_on=['ProvinceId', 'Province', 'ProvinceEn'], right_on=['ProvinceId', 'Province', 'ProvinceEn'])

df_date.to_csv('./result/covid19_thai_province_event_date.csv', encoding='utf-8')