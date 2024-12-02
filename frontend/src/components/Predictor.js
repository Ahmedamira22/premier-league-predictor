import React, { useState } from 'react';

function Predictor() {
  const [predictions, setPredictions] = useState([]); // Stores predictions
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  const handlePredict = async () => {
    setLoading(true); // Start loading
    setError(null); // Reset any errors

    try {
      const response = await fetch('http://127.0.0.1:5000/predict'); // Fetch from Flask API
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setPredictions(data); // Update predictions state
    } catch (err) {
      setError('Failed to fetch predictions. Please try again.');
      console.error(err);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div>
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Loading...' : 'Prediction for 2025'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {predictions.length > 0 && (
        <div>
          <h2>Premier League Top 4 Predictions for 2025:</h2>
          <ol>
            {predictions.map((team, index) => (
              <li key={index}>
                {team.original_team} (Predicted Position: {team.predicted_position.toFixed(2)})
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default Predictor;
