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
now = datetime.now()
now_str = now.strftime('%Y%m%d')

cases = requests.get(url_cases).json()
with open('./data/%s_covid19_th_cases.json' % (now_str), 'w') as json_file:
    json.dump(cases, json_file)

timeline = requests.get(url_timeline).json()
with open('./data/%s_covid19_th_timeline.json' % (now_str), 'w') as json_file:
    json.dump(timeline, json_file)

area = requests.get(url_cases).json()
with open('./data/%s_covid19_th_area.json' % (now_str), 'w') as json_file:
    json.dump(area, json_file)

timeline['df'] = pd.DataFrame(timeline['Data'])
cases['df'] = pd.DataFrame(cases['Data'])
area['df'] = pd.DataFrame(area['Data'])

# load local data
with open('./data/%s_covid19_th_cases.json' % (now_str)) as json_file:
    cases = json.load(json_file)
with open('./data/%s_covid19_th_timeline.json' % (now_str)) as json_file:
    timeline = json.load(json_file)
with open('./data/%s_covid19_th_area.json' % (now_str)) as json_file:
    area = json.load(json_file)

# df = pd.DataFrame(data['Data'])