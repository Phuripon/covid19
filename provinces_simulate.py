import pandas as pd
import numpy as np

# use data from r12
from model.seir import recent_cases_to_doubling_time, get_default_params
from model_run import model_run

input_summary = pd.read_excel('./data/covid19_r12_province_data.xlsx', sheet_name='Summary')
default_doubling_time = 0

# run each area
df_output = pd.DataFrame()
for index, area in input_summary.iterrows():
    # read data of area cases
    df_area_cases = pd.read_excel('./data/covid19_r12_province_data.xlsx', sheet_name=area['sheetname'])
    recent_date = 30
    recent_cases = df_area_cases['TotalConfirmCases'].to_list()[-recent_date:]
    recent_cases.sort(reverse=True)
    # create model input
    model_input = {
        # ref situation
        'area': area['sheetname'],
        'total_confirm_cases': df_area_cases['TotalConfirmCases'].iloc[-1],
        'active_cases': df_area_cases['ActiveCases'].iloc[-1],
        'critical_cases': df_area_cases['CriticalCases'].iloc[-1],
        'death': df_area_cases['Deaths'].iloc[-1],
        'recent_cases': recent_cases,
        # ref site
        'regional_population': area['population'],
        'hospital_market_share': 1,
        # predict period
        'start_date': df_area_cases['ConfirmDate'].iloc[-1],
        'steps': 100,
        # intervention
        'social_distancing': [0, 0, 1],
    }

    # compute doubling time
    doubling_time = recent_cases_to_doubling_time(model_input['recent_cases'], period=7, default=default_doubling_time)
    if area['sheetname'] == 'R12':
        default_doubling_time = doubling_time
    print('Doubling Time ของ %s อยู่ที่ %s วัน' % (area['area'], round(doubling_time, 1)))
    model_input['doubling_time'] = doubling_time
    # run model
    params = get_default_params()
    df_output_area = model_run(model_input, params)

    # add resource inventiry & cap
    df_output_area['bed_capacity'] = df_area_cases['BedCapacity'].iloc[-1]
    df_output_area['bed_available'] = df_output_area['bed_capacity'] - df_output_area['bed_hos']
    df_output_area['bed_available'] = df_output_area['bed_available'].apply(lambda x: max(x, 0))
    df_output_area['bed_icu_capacity'] = df_area_cases['BedICUCapacity'].iloc[-1] * 0.05
    df_output_area['bed_icu_available'] = df_output_area['bed_icu_capacity'] - df_output_area['bed_icu']
    df_output_area['bed_icu_available'] = df_output_area['bed_icu_available'].apply(lambda x: max(x, 0))
    df_output_area['drug_favipiravir_inventory'] = [df_area_cases['FavipiravirInventory'].iloc[-1]] * len(
        df_output_area) - df_output_area['drug_favipiravir'].cumsum()
    df_output_area['drug_favipiravir_inventory'] = df_output_area['drug_favipiravir_inventory'].apply(
        lambda x: max(x, 0))

    # append history data
    df_history = pd.DataFrame({'date': df_area_cases['ConfirmDate'].to_list()[-recent_date:-1],
                               'total_confirm_cases': df_area_cases['TotalConfirmCases'].to_list()[-recent_date:-1]})
    df_output_area = df_history.append(df_output_area)
    df_output_area['area'] = area['area']
    df_output = df_output.append(df_output_area)

# export data
df_output.to_excel('./result/covid19_r12_resource_simulation.xlsx', sheet_name='simulation')

# use resource from r12

# simulate multiple province
# compute resource consumption
# merge to 1 table
