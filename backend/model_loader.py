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
