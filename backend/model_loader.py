import joblib
import os

def load_model():
    """
    Loads the pre-trained F1 Race Predictor model from a .joblib file.

    Returns:
        sklearn.ensemble.GradientBoostingRegressor: The loaded Gradient Boosting Regressor model,
                                                  or None if the model file is not found.
    """
    # Define the directory where the model is saved
    # This path is now relative to the location of this script.
    # Assuming 'models' directory is one level up from the script, e.g.,
    # F1-Predictor/
    # ├── models/
    # │   └── GradientBoosting_F1_Race_Predictor_model.joblib
    # └── scripts/
    #     └── model_loader.py
    # If 'models' is in the same directory as this script, just use 'models'.
    script_dir = os.path.dirname(__file__)
    model_dir = os.path.join(script_dir, '..', 'models') # Go up one level, then into 'models'
    model_filename = 'GradientBoosting_F1_Race_Predictor_model.joblib'
    
    # Construct the full path to the model file
    full_model_path = os.path.join(model_dir, model_filename)

    try:
        # Load the model using joblib
        loaded_model = joblib.load(full_model_path)
        print(f"Model '{model_filename}' loaded successfully from {full_model_path}.")
        return loaded_model
    except FileNotFoundError:
        print(f"Error: Model file not found at '{full_model_path}'.")
        print("Please ensure the path is correct and the model has been saved.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the model: {e}")
        return None



