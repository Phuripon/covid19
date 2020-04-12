from model.seir import gen_initial, summarize_seir, \
    recent_cases_to_doubling_time, SEIR, get_default_params
from load_thai_cases import load_json
import pandas as pd
from datetime import datetime
import numpy as np


def convert_text_to_datetime(x):
    return datetime.strptime(x, '%m/%d/%Y')


# TODO: validate with thailand history
# observed data
# load thai_cases
timeline = load_json('covid19_th_timeline.json')
# create thai_cases df
df_timeline = pd.DataFrame(timeline['Data'])
df_timeline['Date'] = df_timeline['Date'].apply(convert_text_to_datetime)

# predict data
# simulate model
# adjust input
# TODO: compute doubling time from ref situation
model_input = {
    # ref situation
    "doubling_time": 7.5,
    "total_confirm_cases": 2169,
    "active_cases": 1353,
    "critical_cases": 23,
    "death": 23,
    # ref site
    "regional_population": 66558935,
    "hospital_market_share": 1,
    # predict period
    "start_date": pd.to_datetime("2020-04-05"),
    "steps": 300,
    # intervention
    "social_distancing": [0, 0, 1],
}

# Simulation
params = get_default_params()
initial_data, params = gen_initial(params, model_input)
seir_df = SEIR(params, initial_data, model_input['step'])
# Summarize
summary_df = summarize_seir(seir_df)

# fitting

# return model error -> แม่นกี่วัน

# TODO: validate with other country history
# TODO: validate with thai province history

# TODO: define measurement (mse sse)

# TODO: define scope of validate (how long? parameter?)
