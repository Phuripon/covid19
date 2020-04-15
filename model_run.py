from model.seir import gen_initial, summarize_seir, recent_cases_to_doubling_time, get_default_params, SEIR
from model.resource_projection import transform_seir, project_resource, get_resource_consumption
import pandas as pd
import numpy as np


def seir_estimation(params, initial_data, user_input, resource_consumption):
    predict_step = int(user_input.get('steps', params['steps']))
    hospital_market_share = float(user_input.get(
        'hospital_market_share', params['hospital_market_share']))
    seir_df = SEIR(params, initial_data, predict_step)
    hos_load_df = transform_seir(seir_df, params, hospital_market_share)
    resource_projection_df = project_resource(hos_load_df, resource_consumption)

    return seir_df, hos_load_df, resource_projection_df


def seir_df_to_json(seir_df, resource_df):
    seir_json = seir_df.set_index('date').to_json(
        orient='split', date_format='iso')
    resource_json = resource_df.set_index(
        'date').to_json(orient='split', date_format='iso')
    return seir_json, resource_json


def prepare_input(user_input):
    default_params = get_default_params()
    user_input['start_date'] = pd.to_datetime(
        user_input.get('start_date', default_params['today']))
    user_input['social_distancing'] = [
        float(user_input.get('social_distancing',
                             default_params['social_distancing_rate'])),
        float(user_input.get('social_distancing_start',
                             default_params['social_distance_day_start'])),
        float(user_input.get('social_distancing_end',
                             default_params['social_distance_day_end']))
    ]
    user_input['regional_population'] = user_input.get(
        'regional_population', default_params['regional_population'])
    user_input['hospital_market_share'] = user_input.get(
        'hospital_market_share', default_params['hospital_market_share'])
    user_input['doubling_time'] = user_input.get(
        'doubling_time', default_params['doubling_time'])
    user_input['doubling_time'] = user_input.get(
        'doubling_time', default_params['doubling_time'])
    user_input['critical_cases'] = user_input.get(
        'critical_cases', default_params['critical_cases'])
    user_input['death'] = user_input.get(
        'death', default_params['death'])
    return user_input, default_params


def model_run(model_input, params):
    # Model and prediction
    initial_data, params = gen_initial(params, model_input)
    resource_consumption = get_resource_consumption()
    seir_df, hos_load_df, resource_df = seir_estimation(params, initial_data, model_input, resource_consumption)
    # Summarize SEIR
    summary_df = summarize_seir(seir_df)
    # Join with resource projection
    output_df = summary_df.merge(hos_load_df, left_on='date', right_on='date')
    output_df = output_df.merge(resource_df, left_on='date', right_on='date')

    return output_df


# model_input = {
#     # ref situation
#     'area': 'Songkhla',
#     'doubling_time': 7.5,
#     'total_confirm_cases': 37,
#     'active_cases': 18,
#     'critical_cases': 1,  # TODO: optional parameter now not effect
#     'death': 0,
#     'recent_cases': [37,37,37,37,34,29,26,24,23,22],
#     # ref site
#     'regional_population': 1435968,
#     'hospital_market_share': 1,
#     # predict period
#     'start_date': pd.to_datetime('2020-04-07'),
#     'steps': 100,
#     # intervention
#     'social_distancing': [0, 0, 1],
# }

# model_input = {
#     # ref situation
#     'area': 'Yala',
#     'doubling_time': 7.5,
#     'total_confirm_cases': 68,
#     'active_cases': 40,
#     'critical_cases': 1,  # TODO: optional parameter now not effect
#     'death': 1,
#     'recent_cases': [68,56,54,52,49,44,35,35,30,30,28,26],
#     # ref site
#     'regional_population': 536330,
#     'hospital_market_share': 1,
#     # predict period
#     'start_date': pd.to_datetime('2020-04-07'),
#     'steps': 100,
#     # intervention
#     'social_distancing': [0, 0, 1],
# }

model_input = {
    # ref situation
    'area': 'R12',
    'doubling_time': 7.5,
    'total_confirm_cases': 193,
    'active_cases': 115,
    'critical_cases': 4,
    'death': 4,
    'recent_cases': [193, 178, 175, 163, 153, 141, 123, 114, 107, 106],
    # ref site
    'regional_population': 4997037,
    'hospital_market_share': 1,
    # predict period
    'start_date': pd.to_datetime('2020-04-07'),
    'steps': 100,
    # intervention
    'social_distancing': [0, 0, 1],
}

supply_level = {
    'bed_icu': 100,
    'bed': 1000,
    'ventilator': 50,
    'negative_pressure': 10,
    'ppe_mask': 100000,
    'drug_favipiravir': 235285,
}

intervention = [
    {
        'event': 'indonesia',
        'start_date': pd.to_datetime('2020-04-07'),
        'end_date': pd.to_datetime('2020-04-07'),
        'import_per_day': {
            's': 0,
            'e': 0,
            'i': 0,
            'pui': 0,
            'hos_mild': 0,
            'hos_severe': 0,
            'hos_critical': 0,
            'hos_fatal': 0,
            'home_mild': 0,
            'home_severe': 0,
            'hotel_mild': 0,
            'hotel_severe': 0,
            'r_mild_hos': 0,
            'r_mild_home': 0,
            'r_mild_hotel': 0,
            'r_severe_hos': 0,
            'r_severe_home': 0,
            'r_severe_hotel': 0,
            'r_critical_hos': 0,
            'death': 0,
        }
    }
]

if __name__ == '__main__':
    # compute doubling time
    doubling_time = recent_cases_to_doubling_time(model_input['recent_cases'], period=7)
    print('Doubling Time: ', doubling_time)
    model_input['doubling_time'] = doubling_time
    params = get_default_params()
    output_df = model_run(model_input, params)
    last_date = model_input['start_date']
    output_df.to_csv(
        './result/covid19_thai_resource_simulation_%s_%s.csv' % (model_input['area'], last_date.strftime('%Y%m%d')),
        encoding='utf-8')  # TODO: add area nam + doubling time + ref date
