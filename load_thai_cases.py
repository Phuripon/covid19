import urllib
import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime

# url = 'https://opend.data.go.th/get-ckan/datastore_search?resource_id=93f74e67-6f76-4b25-8f5d-b485083100b6&limit=5&q=title:jones'
url_today = 'https://covid19.th-stat.com/api/open/today'
url_timeline = 'https://covid19.th-stat.com/api/open/timeline'
url_cases = 'https://covid19.th-stat.com/api/open/cases'
url_cases_sum = 'https://covid19.th-stat.com/api/open/cases/sum'
url_area = 'https://covid19.th-stat.com/api/open/area'

# update local data
# TODO: backup load data to local with .gitignore
now = datetime.now()
now_str = now.strftime('%Y%m%d')


def write_json(json_data, filename):
    with open('./data/' + filename, 'w') as json_file:
        json.dump(json_data, json_file)
    with open('./data/bk/' + filename, 'w') as json_file:
        json.dump(json_data, json_file)
    return print('Saved: ' + filename)


def load_json(filename):
    with open('./data/' + filename) as json_file:
        return json.load(json_file)


cases = requests.get(url_cases).json()
write_json(cases, '%s_covid19_th_cases.json' % now_str)

timeline = requests.get(url_timeline).json()
write_json(timeline, '%s_covid19_th_timeline.json' % now_str)

area = requests.get(url_cases).json()
write_json(area, '%s_covid19_th_area.json' % now_str)

timeline['df'] = pd.DataFrame(timeline['Data'])
cases['df'] = pd.DataFrame(cases['Data'])
area['df'] = pd.DataFrame(area['Data'])

# load local data
cases = load_json('%s_covid19_th_cases.json' % now_str)
timeline = load_json('%s_covid19_th_timeline.json' % now_str)
area = load_json('%s_covid19_th_area.json' % now_str)

# df = pd.DataFrame(data['Data'])
