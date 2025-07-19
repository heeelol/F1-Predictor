# preprocessing.py

import pandas as pd
import numpy as np
import joblib
import os

# --- Paths to saved preprocessors ---
PREPROCESSOR_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))

# --- Load fitted OneHotEncoder and training feature names ---
try:
    ohe_encoder = joblib.load(os.path.join(PREPROCESSOR_DIR, 'one_hot_encoder.joblib'))
except FileNotFoundError:
    raise FileNotFoundError(f"Error: 'one_hot_encoder.joblib' not found in {PREPROCESSOR_DIR}. Ensure it's saved during training.")

# Scaler is explicitly set to None as it was not used in training.
scaler = None

try:
    TRAINING_FEATURE_NAMES = joblib.load(os.path.join(PREPROCESSOR_DIR, 'training_feature_names.joblib'))
except FileNotFoundError:
    # This list should ideally be saved from your training notebook.
    # Hardcoding as a fallback, but direct saving is preferred for exact consistency.
    TRAINING_FEATURE_NAMES = [
        'Season', 'Round', 'GridPosition', 'Q1_s', 'Q2_s', 'Q3_s',
        'Abbreviation_BOT', 'Abbreviation_BUT', 'Abbreviation_DIR', 'Abbreviation_ERI', 'Abbreviation_GAS',
        'Abbreviation_GIO', 'Abbreviation_GRO', 'Abbreviation_GUT', 'Abbreviation_HAM', 'Abbreviation_HAR',
        'Abbreviation_HUL', 'Abbreviation_KVY', 'Abbreviation_LEC', 'Abbreviation_MAG', 'Abbreviation_MAL',
        'Abbreviation_MAS', 'Abbreviation_MER', 'Abbreviation_NAS', 'Abbreviation_OCO', 'Abbreviation_PAL',
        'Abbreviation_PER', 'Abbreviation_RAI', 'Abbreviation_RIC', 'Abbreviation_ROS', 'Abbreviation_RSS',
        'Abbreviation_SAI', 'Abbreviation_SIR', 'Abbreviation_STE', 'Abbreviation_STR', 'Abbreviation_VAN',
        'Abbreviation_VER', 'Abbreviation_VET', 'Abbreviation_WEH',
        'TeamName_Force India', 'TeamName_Haas F1 Team', 'TeamName_Lotus F1', 'TeamName_Manor Marussia',
        'TeamName_McLaren', 'TeamName_Mercedes', 'TeamName_Racing Point', 'TeamName_Red Bull',
        'TeamName_Red Bull Racing', 'TeamName_Renault', 'TeamName_Sauber', 'TeamName_Toro Rosso', 'TeamName_Williams',
        'EventName_Australian Grand Prix', 'EventName_Austrian Grand Prix', 'EventName_Azerbaijan Grand Prix',
        'EventName_Bahrain Grand Prix', 'EventName_Belgian Grand Prix', 'EventName_Brazilian Grand Prix',
        'EventName_British Grand Prix', 'EventName_Canadian Grand Prix', 'EventName_Chinese Grand Prix',
        'EventName_European Grand Prix', 'EventName_French Grand Prix', 'EventName_German Grand Prix',
        'EventName_Hungarian Grand Prix', 'EventName_Italian Grand Prix', 'EventName_Japanese Grand Prix',
        'EventName_Malaysian Grand Prix', 'EventName_Mexican Grand Prix', 'EventName_Monaco Grand Prix',
        'EventName_Russian Grand Prix', 'EventName_Singapore Grand Prix', 'EventName_Spanish Grand Prix',
        'EventName_United States Grand Prix'
    ]


def preprocess_input(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses raw input data for the F1 Rank Predictor model,
    replicating steps from model training.

    Args:
        data (pd.DataFrame): Raw input data with expected columns.

    Returns:
        pd.DataFrame: Preprocessed DataFrame, ready for model prediction.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input 'data' must be a pandas DataFrame.")
    if data.empty:
        return pd.DataFrame(columns=TRAINING_FEATURE_NAMES)

    df = data.copy()

    # --- Data Cleaning: Handle Missing Values ---
    numerical_cols_to_impute_with_zero = ['GridPosition', 'Position', 'Q1_s', 'Q2_s', 'Q3_s']
    for col in numerical_cols_to_impute_with_zero:
        if col in df.columns and df[col].isna().any():
            df.loc[df[col].isna(), col] = 0.0

    # --- Identify Categorical and Numerical Features ---
    categorical_features_input = ['Abbreviation', 'TeamName', 'EventName']
    numerical_features_input = ['Season', 'Round', 'GridPosition', 'Q1_s', 'Q2_s', 'Q3_s']

    # --- Hot Encode Categorical Features ---
    for col in categorical_features_input:
        if col not in df.columns:
            raise ValueError(f"Missing expected categorical column '{col}' in input data.")

    df_categorical = df[categorical_features_input]
    encoded_features = ohe_encoder.transform(df_categorical)
    encoded_df = pd.DataFrame(
        encoded_features.astype(int),
        columns=ohe_encoder.get_feature_names_out(categorical_features_input),
        index=df.index
    )

    # --- Include Numerical Features (No Scaling) ---
    for col in numerical_features_input:
        if col not in df.columns:
            raise ValueError(f"Missing expected numerical column '{col}' in input data.")

    numerical_df = df[numerical_features_input]

    # --- Concatenate all features ---
    preprocessed_df = pd.concat([numerical_df, encoded_df], axis=1)

    # --- Ensure Column Order Consistency ---
    # Reindex to match the exact order of features used during training.
    # `fill_value=0` handles new categories not seen in training if handle_unknown='ignore'
    final_preprocessed_df = preprocessed_df.reindex(columns=TRAINING_FEATURE_NAMES, fill_value=0)

    return final_preprocessed_df


if __name__ == '__main__':
    # --- Local Test Block ---
    # This section runs only when preprocessing.py is executed directly.
    # It creates dummy preprocessor files and tests the function.

    os.makedirs(PREPROCESSOR_DIR, exist_ok=True)

    # --- Create Dummy OneHotEncoder for Testing ---
    from sklearn.preprocessing import OneHotEncoder

    all_abbreviations = ['BOT', 'BUT', 'DIR', 'ERI', 'GAS', 'GIO', 'GRO', 'GUT', 'HAM', 'HAR',
                         'HUL', 'KVY', 'LEC', 'MAG', 'MAL', 'MAS', 'MER', 'NAS', 'OCO', 'PAL',
                         'PER', 'RAI', 'RIC', 'ROS', 'RSS', 'SAI', 'SIR', 'STE', 'STR', 'VAN',
                         'VER', 'VET', 'WEH', 'UNK']
    all_team_names = ['Force India', 'Haas F1 Team', 'Lotus F1', 'Manor Marussia',
                      'McLaren', 'Mercedes', 'Racing Point', 'Red Bull', 'Red Bull Racing',
                      'Renault', 'Sauber', 'Toro Rosso', 'Williams', 'New Team']
    all_team_names = (all_team_names * ((len(all_abbreviations) // len(all_team_names)) + 1))[:len(all_abbreviations)]

    all_event_names = ['Australian Grand Prix', 'Austrian Grand Prix', 'Azerbaijan Grand Prix',
                       'Bahrain Grand Prix', 'Belgian Grand Prix', 'Brazilian Grand Prix',
                       'British Grand Prix', 'Canadian Grand Prix', 'Chinese Grand Prix',
                       'European Grand Prix', 'French Grand Prix', 'German Grand Prix',
                       'Hungarian Grand Prix', 'Italian Grand Prix', 'Japanese Grand Prix',
                       'Malaysian Grand Prix', 'Mexican Grand Prix', 'Monaco Grand Prix',
                       'Russian Grand Prix', 'Singapore Grand Prix', 'Spanish Grand Prix',
                       'United States Grand Prix', 'New Event']
    all_event_names = (all_event_names * ((len(all_abbreviations) // len(all_event_names)) + 1))[:len(all_abbreviations)]

    dummy_ohe_fit_data = pd.DataFrame({
        'Abbreviation': all_abbreviations,
        'TeamName': all_team_names,
        'EventName': all_event_names
    })
    dummy_ohe = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    dummy_ohe.fit(dummy_ohe_fit_data)
    joblib.dump(dummy_ohe, os.path.join(PREPROCESSOR_DIR, 'one_hot_encoder.joblib'))
    print("Dummy OneHotEncoder created.")

    # --- Create Dummy training_feature_names for Testing ---
    if not os.path.exists(os.path.join(PREPROCESSOR_DIR, 'training_feature_names.joblib')):
        dummy_training_feature_names = [
            'Season', 'Round', 'GridPosition', 'Q1_s', 'Q2_s', 'Q3_s',
            'Abbreviation_BOT', 'Abbreviation_BUT', 'Abbreviation_DIR', 'Abbreviation_ERI', 'Abbreviation_GAS',
            'Abbreviation_GIO', 'Abbreviation_GRO', 'Abbreviation_GUT', 'Abbreviation_HAM', 'Abbreviation_HAR',
            'Abbreviation_HUL', 'Abbreviation_KVY', 'Abbreviation_LEC', 'Abbreviation_MAG', 'Abbreviation_MAL',
            'Abbreviation_MAS', 'Abbreviation_MER', 'Abbreviation_NAS', 'Abbreviation_OCO', 'Abbreviation_PAL',
            'Abbreviation_PER', 'Abbreviation_RAI', 'Abbreviation_RIC', 'Abbreviation_ROS', 'Abbreviation_RSS',
            'Abbreviation_SAI', 'Abbreviation_SIR', 'Abbreviation_STE', 'Abbreviation_STR', 'Abbreviation_VAN',
            'Abbreviation_VER', 'Abbreviation_VET', 'Abbreviation_WEH', 'Abbreviation_UNK',
            'TeamName_Force India', 'TeamName_Haas F1 Team', 'TeamName_Lotus F1', 'TeamName_Manor Marussia',
            'TeamName_McLaren', 'TeamName_Mercedes', 'TeamName_Racing Point', 'TeamName_Red Bull',
            'TeamName_Red Bull Racing', 'TeamName_Renault', 'TeamName_Sauber', 'TeamName_Toro Rosso',
            'TeamName_Williams', 'TeamName_New Team',
            'EventName_Australian Grand Prix', 'EventName_Austrian Grand Prix', 'EventName_Azerbaijan Grand Prix',
            'EventName_Bahrain Grand Prix', 'EventName_Belgian Grand Prix', 'EventName_Brazilian Grand Prix',
            'EventName_British Grand Prix', 'EventName_Canadian Grand Prix', 'EventName_Chinese Grand Prix',
            'EventName_European Grand Prix', 'EventName_French Grand Prix', 'EventName_German Grand Prix',
            'EventName_Hungarian Grand Prix', 'EventName_Italian Grand Prix', 'EventName_Japanese Grand Prix',
            'EventName_Malaysian Grand Prix', 'EventName_Mexican Grand Prix', 'EventName_Monaco Grand Prix',
            'EventName_Russian Grand Prix', 'EventName_Singapore Grand Prix', 'EventName_Spanish Grand Prix',
            'EventName_United States Grand Prix', 'EventName_New Event'
        ]
        joblib.dump(dummy_training_feature_names, os.path.join(PREPROCESSOR_DIR, 'training_feature_names.joblib'))
        print("Dummy training_feature_names created.")
    else:
        print("training_feature_names.joblib already exists.")

    # --- Dummy Raw Input Data for Testing preprocess_input ---
    dummy_raw_data_for_test = pd.DataFrame({
        'Season': [2024, 2024, 2023],
        'Round': [5, 5, 10],
        'GridPosition': [1, np.nan, 15],
        'Position': [1, 2, np.nan],
        'Q1_s': [85.123, 85.543, 90.123],
        'Q2_s': [84.987, 85.321, np.nan],
        'Q3_s': [84.567, 84.890, 89.000],
        'Abbreviation': ['VER', 'LEC', 'NOR'],
        'TeamName': ['Red Bull Racing', 'Ferrari', 'McLaren'],
        'EventName': ['Monaco Grand Prix', 'Monaco Grand Prix', 'British Grand Prix'],
    })

    # Run the preprocessing test
    preprocessed_data_test = preprocess_input(dummy_raw_data_for_test)

    print("\n--- Test Preprocessing Results ---")
    print("Test Preprocessed Data Head (first 5 columns):")
    print(preprocessed_data_test.iloc[:, :5].head())
    print("\nTest Preprocessed Data Tail (last 5 columns):")
    print(preprocessed_data_test.iloc[:, -5:].tail())

    print("\nTest Preprocessed Data Columns (should match TRAINING_FEATURE_NAMES):")
    print(preprocessed_data_test.columns.tolist())
    print(f"Shape of preprocessed data: {preprocessed_data_test.shape}")
    print("Verification: All columns from TRAINING_FEATURE_NAMES present in preprocessed data:",
          all(col in preprocessed_data_test.columns for col in TRAINING_FEATURE_NAMES))
    print("Verification: All columns in preprocessed data are from TRAINING_FEATURE_NAMES and in correct order:",
          TRAINING_FEATURE_NAMES == preprocessed_data_test.columns.tolist())