import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime


def write_json(json_data, filename):
    with open('./data/' + filename, 'w') as json_file:
        json.dump(json_data, json_file)
    with open('./data/bk/' + filename, 'w') as json_file:
        json.dump(json_data, json_file)
    return 'Saved: ' + filename


def load_json(filename):
    with open('./data/' + filename) as json_file:
        return json.load(json_file)


# update data from covid19.th-stat
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

timeline['df'] = pd.DataFrame(timeline['Data'])
cases['df'] = pd.DataFrame(cases['Data'])
area['df'] = pd.DataFrame(area['Data'])

# load local data
load_date = '20200404'
cases = load_json('%s_covid19_th_cases.json' % load_date)
timeline = load_json('%s_covid19_th_timeline.json' % load_date)
area = load_json('%s_covid19_th_area.json' % load_date)

df_cases = pd.DataFrame(cases['Data'])
