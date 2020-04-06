import pandas as pd
import numpy as np
import os
from datetime import datetime


def convert_to_datetime(x):
    return datetime.strptime(x, '%m/%d/%y')


# set folder name
folder_path = '../../git/COVID-19_World_Cases/csse_covid_19_data/csse_covid_19_time_series'
files_name = ['time_series_covid19_confirmed_global.csv', 'time_series_covid19_recovered_global.csv',
              'time_series_covid19_deaths_global.csv']

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# load & melt column to transaction
df_confirm = pd.read_csv('%s/%s' % (folder_path, files_name[0]))
df_confirm = df_confirm.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date',
                             value_name='Confirmed')
df_recovered = pd.read_csv('%s/%s' % (folder_path, files_name[1]))
df_recovered = df_recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date',
                                 value_name='Recovered')
df_death = pd.read_csv('%s/%s' % (folder_path, files_name[2]))
df_death = df_death.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date',
                         value_name='Deaths')

# merge df
df_world_cases = df_confirm.merge(df_recovered, left_on=['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'],
                                  right_on=['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])
df_world_cases = df_world_cases.merge(df_death, left_on=['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'],
                                      right_on=['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])

# convert date string to datetime then sort
df_world_cases['Date'] = df_world_cases['Date'].apply(convert_to_datetime)
df_world_cases = df_world_cases.sort_values(by=['Country/Region', 'Province/State', 'Date'])
df_world_cases = df_world_cases.reset_index(drop=True)

# compute new cases
df_world_cases['New_Cases'] = df_world_cases['Confirmed'].diff().map(lambda x: np.nan if x < 0 else x)

#compute active cases
df_world_cases['Active_Cases'] = df_world_cases.apply(lambda x: x['Confirmed'] - x['Recovered'] - x['Deaths'], axis=1)



# sample = df_world_cases.loc[0:200, ['Country/Region', 'Province/State', 'Date', 'Confirmed']]
# sample['New_Cases'] = sample['Confirmed'].diff().map(lambda x: np.nan if x < 0 else x)
# sample['Confirmed'].diff()

# TODO: compute doubling time for total confirm cases & death & recovered

# export csv
df_world_cases.to_csv('./data/covid19_world_cases.csv', index=False, encoding='utf-8')
last_date =df_world_cases['Date'].max().strftime('%Y%m%d')
df_world_cases.to_csv('./data/bk/%s_covid19_world_cases.csv' % last_date, index=False, encoding='utf-8')