# F1 Race Predictor

## Project Overview

The F1 Race Predictor is a machine learning project designed to forecast Formula 1 race finishing positions. By leveraging pre-race data, primarily from the qualifying session, this model aims to provide data-driven insights into potential race outcomes, offering a unique perspective for F1 enthusiasts and analysts. 

## Features

* **Real-time Data Fetching:** Utilizes the `fastf1` API to retrieve the latest qualifying data for any specified 2025 Grand Prix.

* **Predictive Modeling:** Employs a Gradient Boosting Regressor model trained on data from 2015 to 2024 to predict the exact finishing position for each driver.

* **Key Pre-Race Features:** Predictions are based on crucial pre-race indicators including:
    * Season and Round identifiers
    * Event Name
    * Driver Abbreviation and Team Name
    * Qualifying Grid Position
    * Qualifying Lap Times (individually for Q1, Q2, Q3)

* **Insightful Output:** Provides a concise and clean structured JSON output including:
    * Predicted Race Position
    * Driver Name
    * Team Name

* **Efficient Data Handling:** Benefits from `fastf1`'s internal caching mechanism for faster data retrieval on subsequent requests for the same race data. In the event of cache failure, a csv with race and qualifying data from 2015 up to race 12 of 2025 is included under `notebooks`.

## Technologies Used

### Frontend
* **Language**: JavaScript (ES6+)
* **Bundler**: Vite – For fast development and optimized builds.

* **Core Libraries**:
   * React.js: For building interactive and component-based user interfaces.
   * React DOM: For rendering React components to the browser.

* **Styling**:
   * Tailwind CSS: Utility-first CSS framework for rapid UI development.
   * Autoprefixer: Adds vendor prefixes to CSS automatically.

 * **HTTP Client**:
    * Axios: For making HTTP requests to the backend API.

### Backend

* **Language:** Python 3

* **Core Libraries:**
    * `fastf1`: For accessing Formula 1 data.
    * `pandas`: For robust data manipulation and analysis.
    * `numpy`: For numerical operations.
    * `scikit-learn`: For machine learning model search and implementation (specifically `GradientBoostingRegressor`).
    * `joblib`: For efficient serialization and loading of the trained model.

## Setup and Installation

To get this project up and running on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/heeelol/F1-Race-Predictor
    cd F1-Race-Predictor
    ```

### Frontend

2. **Install Dependencies**
    ```bash
    cd frontend
    npm install
    ```

3. **Start the frontend development server (from the frontend directory)r**
    ```bash
    npm run dev
    ```

### Backend

4.  **Create a Virtual Environment (Recommended):**
    ```bash
    cd ../backend
    python -m venv venv
    ```

5.  **Activate the Virtual Environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

6.  **Install Dependencies:**
    In the `requirements.txt` file contains the necessary dependencies and their respective versions used for this project. 
    ```bash
    pip install -r requirements.txt
    ```

7. **Start the backend server (from the backend directory)**
     ```bash
    py app.py
    ```

8.  **Model and Preprocessor Files:**
    Ensure the trained model (`V1_GradientBoosting_F1_Race_Predictor_model.joblib` or `V2_GradientBoosting_F1_Race_Predictor_model.joblib`), the `one_hot_encoder.joblib`, and `training_feature_names.joblib` are located in the **`models/`** directory at the root level of your project.

    Your project structure should look something like this:

    ```
    F1-RACE-PREDICTOR/
    ├── backend/
    │   ├── app.py                     
    │   ├── model_loader.py
    │   ├── preprocessing.py
    │   └── utils.py
    ├── frontend/
    ├── models/
    │   ├── one_hot_encoder.joblib
    │   ├── training_feature_names.joblib
    │   ├── V1_GradientBoosting_F1_Race_Predictor_model.joblib
    │   └── V2_GradientBoosting_F1_Race_Predictor_model.joblib
    ├── notebooks/
    │   └── data_cache/
    ├── README.md
    └── requirements.txt
    ```

## Usage

The core functionality is exposed via the `get_race_predictions_json` function, which is likely located in `backend/app.py`. This function takes the `year` and `round_number` of an F1 event and returns a JSON string with the predicted results.

Here's how to use it (assuming you're running from the root `F1-RACE-PREDICTOR` directory):

```python
import json
# Adjust the import path based on your actual file structure.
# Assuming get_race_predictions_json is in backend/app.py
from backend.app import get_race_predictions_json 

# Example: Get predictions for the 2023 British Grand Prix (Round 10)
target_year = 2023
target_round = 10 

print(f"Requesting predictions for {target_year} Round {target_round}...")
predicted_results_json = get_race_predictions_json(target_year, target_round)

if predicted_results_json:
    # Parse and pretty-print the JSON output
    parsed_json = json.loads(predicted_results_json)
    print("\nPredicted Race Results (JSON Output):")
    print(json.dumps(parsed_json, indent=4))
else:
    print(f"Failed to retrieve predictions for {target_year} Round {target_round}.")
