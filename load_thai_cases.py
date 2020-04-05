import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime


def write_json(json_data, filename):
    with open('./data/' + filename[9:], 'w') as json_file:
        json.dump(json_data, json_file)
    with open('./data/bk/' + filename, 'w') as json_file:
        json.dump(json_data, json_file)
    return 'Saved: ' + filename


def load_json(filename):
    with open('./data/' + filename) as json_file:
        return json.load(json_file)


def convert_text_to_datetime(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

is_update = False


# update data from covid19.th-stat
if is_update:
    url_today = 'https://covid19.th-stat.com/api/open/today'
    url_timeline = 'https://covid19.th-stat.com/api/open/timeline'
    url_cases = 'https://covid19.th-stat.com/api/open/cases'
    url_cases_sum = 'https://covid19.th-stat.com/api/open/cases/sum'
    url_area = 'https://covid19.th-stat.com/api/open/area'

    cases = requests.get(url_cases).json()
    timeline = requests.get(url_timeline).json()
    area = requests.get(url_area).json()
    cases_sum = requests.get(url_cases_sum).json()

    # def update_th_cases(url):
    #     try:
    #         res = requests.get(url)
    #     except requests.exceptions.ConnectionError:
    #         print("Connection refused")
    #         return []
    #     return res.json()
    #
    # cases = update_th_cases(url_cases)


    # writing local data
    last_data = datetime.strptime(cases['LastData'], '%Y-%m-%d %H:%M:%S')
    last_date = last_data.strftime('%Y%m%d')
    write_json(cases, '%s_covid19_th_cases.json' % last_date)
    write_json(timeline, '%s_covid19_th_timeline.json' % last_date)
    write_json(area, '%s_covid19_th_area.json' % last_date)
    write_json(cases_sum, '%s_covid19_th_cases_sum.json' % last_date)

# load local data
# load_date = '20200404'
cases = load_json('covid19_th_cases.json')
timeline = load_json('covid19_th_timeline.json')
area = load_json('covid19_th_area.json')

# create cases df
df_cases = pd.DataFrame(cases['Data'])
df_cases['ConfirmDate'] = df_cases['ConfirmDate'].apply(convert_text_to_datetime)

# pivot provinceId & confirmDate
df_province_timeline = pd.pivot_table(df_cases, values=['No'],
                                      index=['ProvinceId', 'ConfirmDate'], aggfunc='count')
# rename column
df_province_timeline.columns = ['NewCases']


# add missing date
idx0 = df_cases['ProvinceId'].unique()
idx1 = pd.date_range(df_cases['ConfirmDate'].min(), df_cases['ConfirmDate'].max())
midx = pd.MultiIndex.from_product([idx0, idx1], names=['ProvinceId', 'ConfirmDate'])
df_province_timeline = df_province_timeline.reindex(midx, fill_value=0)
df_province_timeline = df_province_timeline.sort_values(by=['ProvinceId', 'ConfirmDate'])

# find total confirm cases for each province
df_province_timeline['TotalConfirmCases'] = df_province_timeline.groupby(level=0)['NewCases'].cumsum()
df_province_timeline = df_province_timeline.reset_index()

# add label for provinceId
# create master province
province_detail = ['ProvinceId','Province','ProvinceEn']
master_province = df_cases.drop_duplicates(province_detail)[province_detail]
df_province_timeline.merge(master_province, left_on=['ProvinceId'], right_on=['ProvinceId'])
col_prov = ['ProvinceId','Province','ProvinceEn','ConfirmDate','NewCases','TotalConfirmCases']
df_province_timeline = df_province_timeline.merge(master_province, left_on=['ProvinceId'], right_on=['ProvinceId'])
df_province_timeline = df_province_timeline[col_prov]

# export csv
df_province_timeline.to_csv('./result/covid19_thai_province_timeline.csv', encoding='utf-8')