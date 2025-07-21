# preprocessing.py

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import OneHotEncoder # Ensure OneHotEncoder is imported for the test block

# --- Paths to saved preprocessors ---
PREPROCESSOR_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))

# --- Load fitted OneHotEncoder and training feature names ---
try:
    ohe_encoder = joblib.load(os.path.join(PREPROCESSOR_DIR, 'one_hot_encoder.joblib'))
except FileNotFoundError:
    raise FileNotFoundError(f"Error: 'one_hot_encoder.joblib' not found in {PREPROCESSOR_DIR}. Ensure it's saved during training.")

# Scaler is explicitly set to None as it was not used in training.
scaler = None

# --- UPDATE TRAINING_FEATURE_NAMES based on the new provided list ---
# This list MUST exactly match the columns and their order from your trained model's feature set.
TRAINING_FEATURE_NAMES = [
    'Season', 'Round', 'GridPosition', 'Q1_s', 'Q2_s', 'Q3_s', 'Position',
    'Abbreviation_ALB', 'Abbreviation_ALO', 'Abbreviation_ANT', 'Abbreviation_BEA', 'Abbreviation_BOR', 'Abbreviation_BOT', 'Abbreviation_BUT', 'Abbreviation_COL', 'Abbreviation_DEV', 'Abbreviation_DIR', 'Abbreviation_DOO', 'Abbreviation_ERI', 'Abbreviation_FIT', 'Abbreviation_GAS', 'Abbreviation_GIO', 'Abbreviation_GRO', 'Abbreviation_GUT', 'Abbreviation_HAD', 'Abbreviation_HAM', 'Abbreviation_HAR', 'Abbreviation_HUL', 'Abbreviation_KUB', 'Abbreviation_KVY', 'Abbreviation_LAT', 'Abbreviation_LAW', 'Abbreviation_LEC', 'Abbreviation_MAG', 'Abbreviation_MAL', 'Abbreviation_MAS', 'Abbreviation_MAZ', 'Abbreviation_MER', 'Abbreviation_MSC', 'Abbreviation_NAS', 'Abbreviation_NOR', 'Abbreviation_OCO', 'Abbreviation_PAL', 'Abbreviation_PER', 'Abbreviation_PIA', 'Abbreviation_RAI', 'Abbreviation_RIC', 'Abbreviation_ROS', 'Abbreviation_RSS', 'Abbreviation_RUS', 'Abbreviation_SAI', 'Abbreviation_SAR', 'Abbreviation_SIR', 'Abbreviation_STE', 'Abbreviation_STR', 'Abbreviation_TSU', 'Abbreviation_VAN', 'Abbreviation_VER', 'Abbreviation_VET', 'Abbreviation_WEH', 'Abbreviation_ZHO',
    'TeamName_Alfa Romeo Racing', 'TeamName_AlphaTauri', 'TeamName_Alpine', 'TeamName_Aston Martin', 'TeamName_Ferrari', 'TeamName_Force India', 'TeamName_Haas F1 Team', 'TeamName_Kick Sauber', 'TeamName_Lotus F1', 'TeamName_Manor Marussia', 'TeamName_McLaren', 'TeamName_Mercedes', 'TeamName_RB', 'TeamName_Racing Bulls', 'TeamName_Racing Point', 'TeamName_Red Bull', 'TeamName_Red Bull Racing', 'TeamName_Renault', 'TeamName_Sauber', 'TeamName_Toro Rosso', 'TeamName_Williams',
    'EventName_Abu Dhabi Grand Prix', 'EventName_Australian Grand Prix', 'EventName_Austrian Grand Prix', 'EventName_Azerbaijan Grand Prix', 'EventName_Bahrain Grand Prix', 'EventName_Belgian Grand Prix', 'EventName_Brazilian Grand Prix', 'EventName_British Grand Prix', 'EventName_Canadian Grand Prix', 'EventName_Chinese Grand Prix', 'EventName_Dutch Grand Prix', 'EventName_Eifel Grand Prix', 'EventName_Emilia Romagna Grand Prix', 'EventName_European Grand Prix', 'EventName_French Grand Prix', 'EventName_German Grand Prix', 'EventName_Hungarian Grand Prix', 'EventName_Italian Grand Prix', 'EventName_Japanese Grand Prix', 'EventName_Las Vegas Grand Prix', 'EventName_Malaysian Grand Prix', 'EventName_Mexican Grand Prix', 'EventName_Mexico City Grand Prix', 'EventName_Miami Grand Prix', 'EventName_Monaco Grand Prix', 'EventName_Portuguese Grand Prix', 'EventName_Qatar Grand Prix', 'EventName_Russian Grand Prix', 'EventName_Sakhir Grand Prix', 'EventName_Saudi Arabian Grand Prix', 'EventName_Singapore Grand Prix', 'EventName_Spanish Grand Prix', 'EventName_Styrian Grand Prix', 'EventName_São Paulo Grand Prix', 'EventName_Turkish Grand Prix', 'EventName_Tuscan Grand Prix', 'EventName_United States Grand Prix'
]

try:
    # Attempt to load the TRAINING_FEATURE_NAMES from disk,
    # but the hardcoded list above will serve as the primary source now.
    # It's good practice to save this list from your training script as well.
    loaded_training_feature_names = joblib.load(os.path.join(PREPROCESSOR_DIR, 'training_feature_names.joblib'))
    if loaded_training_feature_names != TRAINING_FEATURE_NAMES:
        print("WARNING: Loaded 'training_feature_names.joblib' differs from hardcoded list. Using hardcoded list.")
except FileNotFoundError:
    print(f"WARNING: 'training_feature_names.joblib' not found in {PREPROCESSOR_DIR}. Using hardcoded list.")
except Exception as e:
    print(f"WARNING: Error loading 'training_feature_names.joblib': {e}. Using hardcoded list.")


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
        # Return an empty DataFrame with the correct column structure
        return pd.DataFrame(columns=TRAINING_FEATURE_NAMES)

    df = data.copy()

    # --- Data Cleaning: Handle Missing Values ---
    numerical_cols_to_impute_with_zero = ['GridPosition', 'Position', 'Q1_s', 'Q2_s', 'Q3_s']
    for col in numerical_cols_to_impute_with_zero:
        if col in df.columns and df[col].isna().any():
            df.loc[df[col].isna(), col] = 0.0
        # If the column is missing from the input data entirely, it will be handled by reindex later (filled with 0)

    # --- Identify Categorical and Numerical Features ---
    # These should be the *original* categorical column names, not the encoded ones.
    categorical_features_input = ['Abbreviation', 'TeamName', 'EventName']
    numerical_features_input = ['Season', 'Round', 'GridPosition', 'Q1_s', 'Q2_s', 'Q3_s', 'Position'] # 'Position' is here as it's in TRAINING_FEATURE_NAMES

    # --- Hot Encode Categorical Features ---
    # Ensure all required categorical columns are present for transformation
    for col in categorical_features_input:
        if col not in df.columns:
            # If a categorical column is missing, create it with a default (e.g., 'Unknown')
            # The 'handle_unknown='ignore'' in OneHotEncoder will then convert this to all zeros.
            print(f"WARNING: Missing expected categorical column '{col}' in input data. Adding as 'Unknown'.")
            df[col] = 'Unknown' # Or a specific placeholder known to OHE

    df_categorical = df[categorical_features_input]
    encoded_features = ohe_encoder.transform(df_categorical) # Use the loaded ohe_encoder
    encoded_df = pd.DataFrame(
        encoded_features.astype(int),
        columns=ohe_encoder.get_feature_names_out(categorical_features_input),
        index=df.index
    )

    # --- Include Numerical Features (No Scaling) ---
    numerical_df_columns = []
    for col in numerical_features_input:
        if col in df.columns:
            numerical_df_columns.append(col)
        else:
            print(f"WARNING: Missing expected numerical column '{col}' in input data. It will be created as 0 by reindex.")
            # If a numerical column is missing, reindex will fill it with 0.

    numerical_df = df[numerical_df_columns]


    # --- Concatenate all features ---
    preprocessed_df = pd.concat([numerical_df, encoded_df], axis=1)

    # --- Ensure Column Order Consistency ---
    # Reindex to match the exact order of features used during training.
    # `fill_value=0` handles new categories not seen in training (if handle_unknown='ignore')
    # and any numerical columns missing from the input data.
    final_preprocessed_df = preprocessed_df.reindex(columns=TRAINING_FEATURE_NAMES, fill_value=0)

    return final_preprocessed_df


if __name__ == '__main__':
    # --- Local Test Block ---
    # This section runs only when preprocessing.py is executed directly.
    # It creates dummy preprocessor files and tests the function.

    os.makedirs(PREPROCESSOR_DIR, exist_ok=True)

    # --- Create Dummy OneHotEncoder for Testing ---
    # These lists should include ALL possible categories encountered across your dataset
    # during training, ensuring the OHE is fitted on the complete vocabulary.
    all_abbreviations = [
        'ALB', 'ALO', 'ANT', 'BEA', 'BOR', 'BOT', 'BUT', 'COL', 'DEV', 'DIR',
        'DOO', 'ERI', 'FIT', 'GAS', 'GIO', 'GRO', 'GUT', 'HAD', 'HAM', 'HAR',
        'HUL', 'KUB', 'KVY', 'LAT', 'LAW', 'LEC', 'MAG', 'MAL', 'MAS', 'MAZ',
        'MER', 'MSC', 'NAS', 'NOR', 'OCO', 'PAL', 'PER', 'PIA', 'RAI', 'RIC',
        'ROS', 'RSS', 'RUS', 'SAI', 'SAR', 'SIR', 'STE', 'STR', 'TSU', 'VAN',
        'VER', 'VET', 'WEH', 'ZHO', 'UNK' # Added UNK for robustness in dummy data
    ]
    all_team_names = [
        'Alfa Romeo Racing', 'AlphaTauri', 'Alpine', 'Aston Martin', 'Ferrari',
        'Force India', 'Haas F1 Team', 'Kick Sauber', 'Lotus F1', 'Manor Marussia',
        'McLaren', 'Mercedes', 'RB', 'Racing Bulls', 'Racing Point', 'Red Bull',
        'Red Bull Racing', 'Renault', 'Sauber', 'Toro Rosso', 'Williams', 'New Team' # Added New Team
    ]
    all_event_names = [
        'Abu Dhabi Grand Prix', 'Australian Grand Prix', 'Austrian Grand Prix',
        'Azerbaijan Grand Prix', 'Bahrain Grand Prix', 'Belgian Grand Prix',
        'Brazilian Grand Prix', 'British Grand Prix', 'Canadian Grand Prix',
        'Chinese Grand Prix', 'Dutch Grand Prix', 'Eifel Grand Prix',
        'Emilia Romagna Grand Prix', 'European Grand Prix', 'French Grand Prix',
        'German Grand Prix', 'Hungarian Grand Prix', 'Italian Grand Prix',
        'Japanese Grand Prix', 'Las Vegas Grand Prix', 'Malaysian Grand Prix',
        'Mexican Grand Prix', 'Mexico City Grand Prix', 'Miami Grand Prix',
        'Monaco Grand Prix', 'Portuguese Grand Prix', 'Qatar Grand Prix',
        'Russian Grand Prix', 'Sakhir Grand Prix', 'Saudi Arabian Grand Prix',
        'Singapore Grand Prix', 'Spanish Grand Prix', 'Styrian Grand Prix',
        'São Paulo Grand Prix', 'Turkish Grand Prix', 'Tuscan Grand Prix',
        'United States Grand Prix', 'New Event' # Added New Event
    ]
    
    # Create dummy data for fitting the OneHotEncoder with ALL possible categories
    # Use the longest list's length to ensure all categories are covered, repeating others if needed
    max_len = max(len(all_abbreviations), len(all_team_names), len(all_event_names))
    
    dummy_ohe_fit_data = pd.DataFrame({
        'Abbreviation': (all_abbreviations * ((max_len // len(all_abbreviations)) + 1))[:max_len],
        'TeamName': (all_team_names * ((max_len // len(all_team_names)) + 1))[:max_len],
        'EventName': (all_event_names * ((max_len // len(all_event_names)) + 1))[:max_len]
    })
    
    # IMPORTANT: Set drop=None for dummy_ohe to ensure it generates all columns for testing consistency
    # with the provided TRAINING_FEATURE_NAMES, which appear to contain all categories.
    dummy_ohe = OneHotEncoder(drop=None, sparse_output=False, handle_unknown='ignore')
    dummy_ohe.fit(dummy_ohe_fit_data)
    joblib.dump(dummy_ohe, os.path.join(PREPROCESSOR_DIR, 'one_hot_encoder.joblib'))
    print("Dummy OneHotEncoder created with all categories and saved.")

    # --- Save TRAINING_FEATURE_NAMES for Testing ---
    # This ensures the test block uses the correct feature names.
    joblib.dump(TRAINING_FEATURE_NAMES, os.path.join(PREPROCESSOR_DIR, 'training_feature_names.joblib'))
    print("Dummy training_feature_names saved.")


    # --- Dummy Raw Input Data for Testing preprocess_input ---
    # This data should resemble what your raw input to the prediction function would look like.
    dummy_raw_data_for_test = pd.DataFrame({
        'Season': [2024, 2024, 2023, 2025],
        'Round': [5, 5, 10, 1],
        'GridPosition': [1, np.nan, 15, 5],
        'Position': [1, 2, np.nan, 8], # Target variable example
        'Q1_s': [85.123, 85.543, 90.123, np.nan],
        'Q2_s': [84.987, 85.321, np.nan, 70.0],
        'Q3_s': [84.567, 84.890, 89.000, 65.0],
        'Abbreviation': ['VER', 'LEC', 'NOR', 'NEW'], # 'NEW' is an unknown abbreviation to test handle_unknown
        'TeamName': ['Red Bull Racing', 'Ferrari', 'McLaren', 'New Team'], # 'New Team' is a known dummy team
        'EventName': ['Monaco Grand Prix', 'Monaco Grand Prix', 'British Grand Prix', 'New Event'], # 'New Event' is a known dummy event
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