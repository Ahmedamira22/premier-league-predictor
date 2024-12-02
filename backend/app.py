from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from premier_league_model import load_model_and_data, predict_top_teams

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and prepare data
model, X_train = load_model_and_data()

@app.route('/predict', methods=['GET'])
def predict():
    predictions = predict_top_teams(model, X_train)
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
