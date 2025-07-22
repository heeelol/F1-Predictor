from flask import Flask, request, jsonify
from flask_cors import CORS

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
        'rankings': [
            {'position': 1, 'driver': 'Max Verstappen', 'team': 'Red Bull'},
            {'position': 2, 'driver': 'Lewis Hamilton', 'team': 'Mercedes'},
            {'position': 3, 'driver': 'Charles Leclerc', 'team': 'Ferrari'},
            {'position': 4, 'driver': 'Lando Norris', 'team': 'McLaren'},
            {'position': 5, 'driver': 'Oscar Piastri', 'team': 'McLaren'},
            {'position': 6, 'driver': 'George Russell', 'team': 'Mercedes'},
            {'position': 7, 'driver': 'Carlos Sainz', 'team': 'Ferrari'},
            {'position': 8, 'driver': 'Fernando Alonso', 'team': 'Aston Martin'},
            {'position': 9, 'driver': 'Lance Stroll', 'team': 'Aston Martin'},
            {'position': 10, 'driver': 'Pierre Gasly', 'team': 'Alpine'}
        ]
    }
    
    return jsonify(prediction_result)

if __name__ == '__main__':
    app.run(debug=True)