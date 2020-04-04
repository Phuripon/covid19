import pandas as pd

## SEIR MODEL ##

def run(params):
    # default_params = get_default()
    # params = update_params(params)

    SEIR_df = SEIR(params)
    # TODO: Sumup table before resource projection
    # input_df['pt_hos_eod_mild'] = SEIR_df['']
    # input_df['pt_hos_eod_severe'] = SEIR_df['']

    # resource_projection_df = project_resource(SEIR_df)

    # return resource_projection_df
    return SEIR_df


sample_initial_data = {
    'date': pd.to_datetime('31-03-2020'),
    's': 10000,
    'e': 20,
    'i': 2,
    'pui': 0,
    'hos_mild': 100,
    'hos_severe': 20,
    'hos_critical': 5,
    'hos_fatal': 5,
    'home_mild': 0,
    'home_severe': 0,
    'hotel_mild': 0,
    'hotel_severe': 0,
    'r_mild_hos': 0,
    'r_mild_home': 0,
    'r_mild_severe': 0,
    'r_severe_hos': 0,
    'r_severe_home': 0,
    'r_severe_hotel': 0,
    'r_critical_hos': 0,
    'death': 0
}
    # out_df.iloc[-1] = []
    # compute initial value
    step = 1
    for t in range(step):
        sod = out_df.iloc[-1]
        params = [2.2]
        diff = get_differentials(params, sod)
        # print(sod[1:])
        # print(diff)
        # print(sod[1:] + diff)
        eod = sod[1:] + diff
        out_df = out_df.append(eod, ignore_index=True)
        # TODO: add date
        print(out_df)


def SEIR(params):
    # do thing
    # TODO: Compute initial value r0, e, i, pui
    initial_data = {
        'date': pd.to_datetime('31-03-2020'),
        's': 10000,
        'e': 20,
        'i': 2,
        'pui': 0,
        'hos_mild': 100,
        'hos_severe': 20,
        'hos_critical': 5,
        'hos_fatal': 5,
        'home_mild': 0,
        'home_severe': 0,
        'hotel_mild': 0,
        'hotel_severe': 0,
        'r_mild_hos': 0,
        'r_mild_home': 0,
        'r_mild_severe': 0,
        'r_severe_hos': 0,
        'r_severe_home': 0,
        'r_severe_hotel': 0,
        'r_critical_hos': 0,
        'death': 0
    }
    out_df = pd.DataFrame.from_dict([initial_data])
    return out_df

# fixed parameter
incubation_period = 6.1 #day
infectious_period = 2.3 #day

# adjustable parameter
cfr = 0.023
p_mild_case = 0.81
p_severe_case = 0.14
all_fatal_case = 0.05
p_criticall_case = all_fatal_case - cfr
p_fatal_case = 0.023
regional_population = 66000000
LOS_mild = 14 #day


def compute_r0(doublng_time):


def get_differentials(params, step):
    # params
    r0 = params[0]
    D_incubation = 6.1
    D_infectious = 2.3
    d_test = 2
    d_death = 28
    los_hos_mild = 14
    los_hos_severe = 28
    los_hos_critical = 28
    los_home_mild = 7
    los_home_severe = 7
    los_hotel_mild = 7
    los_hotel_severe = 7
    CFR = 0.023
    P_CRITICAL = 0.05
    P_SEVERE = 0.14
    P_MILD = 0.81
    P_MILD_HOTEL = 0
    P_MILD_HOME = 0
    P_SEVERE_HOTEL = 0
    P_SEVERE_HOME = 0
    n = 10000

    sigma = 1 / D_incubation
    gamma = 1 / D_infectious
    beta = r0 * gamma

    # start of day
    s = step.s
    e = step.e
    i = step.i
    pui = step.pui
    hos_mild = step.hos_mild
    hos_severe = step.hos_severe
    hos_critical = step.hos_critical
    hos_fatal = step.hos_fatal
    home_mild = step.home_mild
    home_severe = step.home_severe
    hotel_mild = step.hotel_mild
    hotel_severe = step.hotel_severe

    # percentage of severity
    p_fatal = CFR
    p_critical = P_CRITICAL - p_fatal
    p_severe = P_SEVERE
    p_mild = 1 - p_severe - p_critical - p_fatal

    # transfer pt to home or hotel (only mild & severe)
    p_mild_hotel = P_MILD_HOTEL
    p_mild_home = P_MILD_HOME
    p_mild_hos = 1 - p_mild_home - p_mild_hotel
    p_severe_hotel = P_SEVERE_HOTEL
    p_severe_home = P_SEVERE_HOME
    p_severe_hos = 1 - p_severe_home - p_severe_hotel

    # compute diff in this period
    diff_s = -beta * i * s / n
    diff_e = beta * i * s / n - sigma * e
    diff_i = sigma * e - gamma * i
    diff_pui = gamma * i - (1 / d_test) * pui
    diff_hos_mild = (
            p_mild * (1 / d_test) * pui
            - p_mild_home * (1 / (los_hos_mild - los_home_mild)) * hos_mild
            - p_mild_hotel * (1 / (los_hos_mild - los_hotel_mild)) * hos_mild
            - (1 / los_hos_mild) * hos_mild
    )
    diff_hos_severe = (
            p_severe * (1 / d_test) * pui
            - p_severe_home * (1 / (los_hos_severe - los_home_severe)) * hos_severe
            - p_severe_hotel * (1 / (los_hos_severe - los_hotel_severe)) * hos_severe
            - (1 / los_hos_severe) * hos_severe
    )
    diff_hos_critical = p_critical * (1 / d_test) * pui - (1 / los_hos_critical) * hos_critical
    diff_hos_fatal = p_fatal * (1 / d_test) * pui - (1 / d_death) * hos_fatal
    diff_home_mild = (
            p_mild_home * (1 / (los_hos_mild - los_home_mild)) * hos_mild
            - (1 / (los_hos_mild - los_home_mild)) * home_mild
    )
    diff_home_severe = (
            p_severe_home * (1 / (los_hos_severe - los_home_severe)) * hos_severe
            - (1 / (los_hos_severe - los_home_severe)) * home_severe
    )
    diff_hotel_mild = (
            p_mild_hotel * (1 / (los_hos_mild - los_hotel_mild)) * hos_mild
            - (1 / (los_hos_mild - los_hotel_mild)) * hotel_mild
    )
    diff_hotel_severe = (
            p_severe_hotel * (1 / (los_hos_severe - los_hotel_severe)) * hos_severe
            - (1 / (los_hos_severe - los_hotel_severe)) * hotel_severe
    )
    diff_r_mild_hos = (1 / los_hos_mild) * hos_mild
    diff_r_mild_home = (1 / (los_hos_mild - los_home_mild)) * home_mild
    diff_r_mild_hotel = (1 / (los_hos_mild - los_hotel_mild)) * hotel_mild
    diff_r_severe_hos = (1 / los_hos_severe) * hos_severe
    diff_r_severe_home = (1 / (los_hos_severe - los_home_severe)) * home_severe
    diff_r_severe_hotel = (1 / (los_hos_severe - los_hotel_severe)) * hotel_severe
    diff_r_critical = (1 / los_hos_critical * hos_critical)
    diff_death = (1 / d_death) * hos_fatal

    # compute new confirm case for resource projection
    new_hos_mild = p_mild * (1 / d_test) * pui
    new_hos_severe = p_severe * (1 / d_test) * pui
    new_hos_critical = p_critical * (1 / d_test) * pui + p_fatal * (1 / d_test) * pui

    return [diff_s, diff_e, diff_i, diff_pui, diff_hos_mild, diff_hos_severe, diff_hos_critical,
            diff_hos_fatal, diff_home_mild, diff_home_severe, diff_hotel_mild, diff_hotel_severe,
            diff_r_mild_hos, diff_r_mild_home, diff_r_mild_hotel, diff_r_severe_hos,
            diff_r_severe_home, diff_r_severe_hotel, diff_r_critical, diff_death]



## Resource Projection ##

# mock up
SEIR_df[:1] =
{'date':'31-03-2020',
 'pt_hos_eod_mild':100,
 'pt_hos_eod_severe':20,
 'pt_hos_eod_critical':5,
 'pt_hos_new_mild':10,
 'pt_hos_new_severe':2,
 'pt_hos_new_critical':1,
 'pt_hos_neg_case':1000,
 'pt_hos_pui':600}

sample_SEIR_row = {
  'date':pd.to_datetime('31-03-2020'),
  'pt_hos_eod_mild':100,
  'pt_hos_eod_severe':20,
  'pt_hos_eod_critical':5,
  'pt_hos_new_mild':10,
  'pt_hos_new_severe':2,
  'pt_hos_new_critical':1,
  'pt_hos_neg_case':1000,
  'pt_hos_pui':600
}
SEIR_sample_df = pd.DataFrame.from_dict([sample_SEIR_row]*3)


def project_resource(SEIR_df):
  resources_name = [
    'icu_bed',
    'hospital_bed',
    'ppe_gloves'
  ]
  resources_df = pd.DataFrame()
  resources_df['date'] = SEIR_df['date']
  resources_df['icu_bed'] = SEIR_df['pt_hos_new_severe'] + SEIR_df['pt_hos_new_critical']
  resources_df['ppe_gloves'] = SEIR_df['pt_hos_new_mild']*3 + SEIR_df['pt_hos_new_severe']*6 + SEIR_df['pt_hos_new_critical']*14 + SEIR_df['pt_hos_eod_severe']*6 + SEIR_df['pt_hos_eod_critical']*14
  return resources_df
