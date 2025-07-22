import pandas as pd
import numpy as np
import joblib
import fastf1
import os
import time
import sys



def get_name(year, round):

    try:
        sess = fastf1.get_session(year, round, 'Q')
        sess.load(telemetry=False, laps=True, weather=False)

        if sess.laps is None:
            print("No lap data available for this session.")
            return pd.DataFrame(columns=["Abbreviation", "FullName"])

        drivers = sess.laps['Driver'].unique()

        driver_data = []
        for drv in drivers:
            info = sess.get_driver(drv)
            driver_data.append({
                "Abbreviation": info['Abbreviation'],
                "FullName": info['FullName']
            })

        return pd.DataFrame(driver_data)

    except Exception as e:
        print(f"Error loading session: {e}")
        return pd.DataFrame(columns=["Abbreviation", "FullName"])
    
def format_prediction_output(merged_df):
    top = merged_df.sort_values("PredictedPosition_int")

    rankings = []
    for _, row in top.iterrows():
        rankings.append({
            'position': row['PredictedPosition_int'],
            'driver': row['FullName'],
            'team': row['TeamName']
        })

    return rankings

def get_predictions(year, round):

    fastf1.set_log_level('ERROR')
    #fastf1.Cache.enable_cache('./cache') Commented out since we experience caching issues
    print("\nFastF1 log level set to ERROR. FastF1 cache enabled.")
    # Adjust sys.path to ensure modules in 'backend' are found
    script_dir = os.path.dirname(__file__)
    backend_dir = os.path.abspath(os.path.join(script_dir, '..', 'backend'))
    if backend_dir not in sys.path:
        sys.path.append(backend_dir)
    # Import the preprocessor and model loader
    from preprocessing import preprocess_input # Import your preprocessing function
    from model_loader import load_model  

    quali_session = fastf1.get_session(year, round, 'Q')
    quali_session.load(telemetry=False, laps=False, weather=False) 

    results_df = quali_session.results.copy()
    results_df['Season'] = year
    results_df['Round'] = round
    results_df['EventName'] = quali_session.event['EventName']

    
    results_df['Q1_s'] = results_df['Q1'].dt.total_seconds().fillna(9999.0)
    results_df['Q2_s'] = results_df['Q2'].dt.total_seconds().fillna(9999.0)
    results_df['Q3_s'] = results_df['Q3'].dt.total_seconds().fillna(9999.0)

    results_df = results_df[[
        'Season', 
        'Round',
        'EventName',
        'Abbreviation', 
        'TeamName',
        'GridPosition', 
        'Q1_s', 
        'Q2_s',
        'Q3_s',
    ]]
    results_df['GridPosition'] = [float(i) for i in range(1, 21)]

    results_df = pd.DataFrame(results_df)

    preprocessed_data = preprocess_input(results_df)
    preprocessed_data = preprocessed_data.drop('Position', axis=1)
    model_path = os.path.join(backend_dir, '../models', 'V1_GradientBoosting_F1_Race_Predictor_model.joblib')
    model = load_model(model_path, verbose=True)
    predictions = model.predict(preprocessed_data)

    new_df = results_df.copy()[['Abbreviation', 'TeamName']]
    new_df['PredictedPosition'] = predictions
    new_df.sort_values(by='PredictedPosition', inplace=True)
    new_df['PredictedPosition_int'] = [int(i) for i in range(1, 21)]

    name_df = get_name(year, round)
    
    merged_df = pd.merge(new_df, name_df, on='Abbreviation', how='left')
    
    return format_prediction_output(merged_df)