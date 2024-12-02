import pandas as pd
import xgboost as xgb
import numpy as np

def load_model_and_data():
    # Load the dataset
    data = pd.read_csv('1996-2024.csv')

    # Prepare training data
    X = data.drop(columns=['position', 'notes'])
    X_encoded = pd.get_dummies(X, columns=['team'])
    X_train = X_encoded[X['season_end_year'] <= 2020]
    
    # Load trained model
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    y_train = data['position'][X['season_end_year'] <= 2020]
    model.fit(X_train, y_train)

    return model, X_train

def predict_top_teams(model, X_train):
    # Prepare 2025 data
    data = pd.read_csv('1996-2024.csv')
    new_data = data[data['season_end_year'] == 2024].copy()
    new_data['season_end_year'] = 2025
    new_data['original_team'] = new_data['team']

    # One-Hot Encoding for new data
    new_data_encoded = pd.get_dummies(new_data, columns=['team'])
    for col in X_train.columns:
        if col not in new_data_encoded.columns:
            new_data_encoded[col] = 0
    new_data_encoded = new_data_encoded[X_train.columns]

    # Make predictions
    predictions = model.predict(new_data_encoded)
    new_data['predicted_position'] = predictions
    new_data = new_data.sort_values('predicted_position')

    # Extract top 4 teams
    top_teams = new_data[['original_team', 'predicted_position']].head(4).to_dict(orient='records')
    return top_teams
