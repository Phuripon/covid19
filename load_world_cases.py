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

# group by country
df_world_cases = df_world_cases.groupby(['Country/Region', 'Date']).sum()
df_world_cases = df_world_cases.reset_index()

# filter only country over 1000 cases
pivot_country_cases = pd.pivot_table(df_world_cases, values=['Confirmed'], index=['Country/Region'], aggfunc='max')
country_filter = pivot_country_cases.index[pivot_country_cases['Confirmed'] > 1000].to_list()
df_world_cases = df_world_cases[df_world_cases['Country/Region'].isin(country_filter)]

# convert date string to datetime then sort
df_world_cases['Date'] = df_world_cases['Date'].apply(convert_to_datetime)
df_world_cases = df_world_cases.sort_values(by=['Country/Region', 'Date'])
df_world_cases = df_world_cases.reset_index(drop=True)

# compute new cases
df_world_cases['New_Cases'] = df_world_cases['Confirmed'].diff().map(lambda x: np.nan if x < 0 else x)

# compute active cases
df_world_cases['Active_Cases'] = df_world_cases.apply(lambda x: x['Confirmed'] - x['Recovered'] - x['Deaths'], axis=1)

# compute day after 100 cases
df_world_cases['over_100cases'] = df_world_cases['Confirmed'].apply(lambda x: 1 if x > 100 else 0)
df_world_cases = df_world_cases.groupby(['Country/Region', 'Date']).sum()
df_world_cases['Day_after_100cases'] = df_world_cases.groupby(level=0)['over_100cases'].cumsum() - 1
df_world_cases = df_world_cases.reset_index()

# Remove unnecessary field
df_world_cases = df_world_cases[
    ['Country/Region', 'Date', 'Day_after_100cases', 'Confirmed', 'Recovered', 'Deaths', 'Active_Cases', 'New_Cases']]


# compute doubling time for confirm cases
def compute_confirmed_doubling_time(row):
    period = 7
    if (row['Confirmed'] > row['Confirmed_7day_before']) & (row['Confirmed'] > 0) & (row['Confirmed_7day_before'] > 0):
        return (period - 1) * (np.log(2) / np.log(row['Confirmed'] / row['Confirmed_7day_before']))
    else:
        return np.nan


df_world_cases['Confirmed_7day_before'] = pd.Series([0] * 6).append(df_world_cases['Confirmed'])[
                                          :len(df_world_cases)].reset_index(drop=True)
df_world_cases['Confirmed_Doubling_Time'] = df_world_cases.apply(compute_confirmed_doubling_time, axis=1)


# compute doubling time for recover cases
def compute_recovered_doubling_time(row):
    period = 7
    if (row['Recovered'] > row['Recovered_7day_before']) & (row['Recovered'] > 0) & (row['Recovered_7day_before'] > 0):
        return (period - 1) * (np.log(2) / np.log(row['Recovered'] / row['Recovered_7day_before']))
    else:
        return np.nan


df_world_cases['Recovered_7day_before'] = pd.Series([0] * 6).append(df_world_cases['Recovered'])[
                                          :len(df_world_cases)].reset_index(drop=True)
df_world_cases['Recovered_Doubling_Time'] = df_world_cases.apply(compute_recovered_doubling_time, axis=1)


# compute doubling time for death
def compute_death_doubling_time(row):
    period = 7
    if (row['Deaths'] > row['Deaths_7day_before']) & (row['Deaths'] > 0) & (row['Deaths_7day_before'] > 0):
        return (period - 1) * (np.log(2) / np.log(row['Deaths'] / row['Deaths_7day_before']))
    else:
        return np.nan


df_world_cases['Deaths_7day_before'] = pd.Series([0] * 6).append(df_world_cases['Deaths'])[
                                       :len(df_world_cases)].reset_index(drop=True)
df_world_cases['Deaths_7day_Doubling_Time'] = df_world_cases.apply(compute_death_doubling_time, axis=1)

# export csv
df_world_cases.to_csv('./data/covid19_world_cases.csv', index=False, encoding='utf-8')
last_date = df_world_cases['Date'].max().strftime('%Y%m%d')
df_world_cases.to_csv('./data/bk/%s_covid19_world_cases.csv' % last_date, index=False, encoding='utf-8')

# show all columns
pd.set_option("max_rows", None)
pd.set_option("max_columns", None)
