"""
Simple database module for storing predictions
"""
import json
import os
from datetime import datetime

PREDICTIONS_FILE = "predictions.json"

def load_predictions():
    """Load all predictions from file"""
    if os.path.exists(PREDICTIONS_FILE):
        try:
            with open(PREDICTIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_predictions(predictions):
    """Save predictions to file"""
    with open(PREDICTIONS_FILE, 'w') as f:
        json.dump(predictions, f, indent=2)

def add_prediction(username, features, prediction, probability):
    """Add a new prediction to the database"""
    predictions = load_predictions()
    
    prediction_record = {
        "id": len(predictions) + 1,
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "features": features,
        "prediction": int(prediction),
        "probability_no_diabetes": float(probability[0]),
        "probability_diabetes": float(probability[1])
    }
    
    predictions.append(prediction_record)
    save_predictions(predictions)
    return prediction_record

def get_user_predictions(username):
    """Get all predictions for a specific user
    
    Filters predictions from predictions.json where username exactly matches.
    This ensures users can only see their own predictions.
    
    Parameters
    ----------
    username : str
        The username to filter predictions by (exact match required)
    
    Returns
    -------
    list
        List of prediction dictionaries matching the username
    """
    predictions = load_predictions()
    # Filter by exact username match from predictions.json
    return [p for p in predictions if p.get("username") == username]

def get_all_predictions():
    """Get all predictions (admin only)"""
    return load_predictions()

def get_statistics():
    """Get prediction statistics"""
    predictions = load_predictions()
    
    if not predictions:
        return {
            "total": 0,
            "high_risk": 0,
            "low_risk": 0,
            "unique_users": 0
        }
    
    high_risk = sum(1 for p in predictions if p.get("prediction") == 1)
    low_risk = sum(1 for p in predictions if p.get("prediction") == 0)
    unique_users = len(set(p.get("username") for p in predictions))
    
    return {
        "total": len(predictions),
        "high_risk": high_risk,
        "low_risk": low_risk,
        "unique_users": unique_users,
        "high_risk_percentage": (high_risk / len(predictions) * 100) if predictions else 0
    }




