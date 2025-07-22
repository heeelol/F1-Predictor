from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_predictions

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    race = data['race']
    

    #Replace this with the data from the ML model
    prediction_result = {
        'race': race,
        'prediction': f'Prediction for {race} completed!',
        'rankings': get_predictions(2025, int(race))
    }
    
    return jsonify(prediction_result)

if __name__ == '__main__':
    app.run(debug=True)