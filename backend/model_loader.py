import joblib
import os

def load_model(model_path=None, verbose=True):
    """
    Loads the pre-trained F1 Race Predictor model from a .joblib file.

    Args:
        model_path (str, optional): Custom path to the .joblib model file.
                                    If None, it uses the default path under ../models/.
        verbose (bool): If True, prints status messages.

    Returns:
        sklearn.ensemble.GradientBoostingRegressor: The loaded model, or None if loading fails.
    """
    if model_path is None:
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, '..', 'models', 'GradientBoosting_F1_Race_Predictor_model.joblib')

    try:
        loaded_model = joblib.load(model_path)
        if verbose:
            print(f"✅ Model loaded successfully from: {model_path}")
        return loaded_model
    except FileNotFoundError:
        if verbose:
            print(f"❌ Model file not found at: {model_path}")
        return None
    except Exception as e:
        if verbose:
            print(f"❌ Error loading model from {model_path}: {e}")
        return None

if __name__ == '__main__':
    # This block will only run when the script is executed directly (e.g., python model_loader.py)
    # It will NOT run when the script is imported as a module into another script.

    print("--- Testing model_loader.py ---")

    # --- Test 1: Attempt to load the default model ---
    print("\nAttempting to load default model...")
    model = load_model()

    if model:
        print("Default model loading test: SUCCESS!")
        # You can add more checks here, e.g., print model type or a dummy prediction
        # print(f"Loaded model type: {type(model)}")
        # If you have sample preprocessed data, you could even try:
        # try:
        #     dummy_prediction = model.predict(some_dummy_preprocessed_data)
        #     print(f"Dummy prediction successful (first value): {dummy_prediction[0]}")
        # except Exception as e:
        #     print(f"Error making dummy prediction: {e}")
    else:
        print("Default model loading test: FAILED.")
        print("Please ensure 'GradientBoosting_F1_Race_Predictor_model.joblib' exists in the '../models/' directory relative to this script.")


    # --- Test 2: (Optional) Test with a non-existent path to verify error handling ---
    print("\nAttempting to load a non-existent model (expecting failure)...")
    non_existent_model = load_model(model_path="./non_existent_model.joblib")
    if non_existent_model is None:
        print("Non-existent model loading test: SUCCESS (correctly failed as expected).")
    else:
        print("Non-existent model loading test: FAILED (loaded something unexpectedly).")

    print("\n--- Model loader test complete ---")