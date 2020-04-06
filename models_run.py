from method.seir import gen_initial, prepare_input, seir_estimation, seir_df_to_json, summarize_seir, recent_cases_to_doubling_time

# mock user
user_input = {
    "doubling_time": 7.5,
    "social_distancing": 0,
    "social_distancing_start": 0,
    "social_distancing_end": 1,
    "hospital_market_share": 1,
    "start_date": "2020-04-05",
    "steps": 300,
    "regional_population": 66558935,
    "total_confirm_cases": 2169,
    "active_cases": 1353,
    "critical_cases": 23,
    "death": 23
}

if __name__ == '__main__':
    # Model and prediction
    user_input, default_params = prepare_input(user_input)
    initial_data, params = gen_initial(default_params, user_input)
    seir_df, hos_load_df, resource_df = seir_estimation(
        params, initial_data, user_input
    )
    # Summarize SEIR
    summary_df = summarize_seir(seir_df)
    # Join with resource projection
    output_df = summary_df.merge(hos_load_df, left_on='date', right_on='date')
    output_df = output_df.merge(resource_df, left_on='date', right_on='date')
    output_df.to_csv('./result/covid19_thai_resource_simulation.csv', encoding='utf-8')
