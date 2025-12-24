"""
Scoring script for Azure ML endpoint
This script runs predictions on the deployed model
"""

import json
import pandas as pd
import joblib
import os
from datetime import datetime


def init():
    """
    Initialize the model when endpoint starts
    """
    global model, service_description_mapping, season_mapping
    
    # Load the model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "xgboost_cpu_forecaster.pkl")
    model = joblib.load(model_path)
    
    # Mappings
    service_description_mapping = {
        "CPU_Usage": 1,
        "Windows_CPU_Usage": 2,
        "CPU_Usage_SQL": 3
    }
    
    season_mapping = {
        "winter": 0, "spring": 1, "summer": 2, "autumn": 3,
        "Winter": 0, "Spring": 1, "Summer": 2, "Autumn": 3
    }
    
    print("Model loaded successfully")


def run(raw_data):
    """
    Predict CPU usage for given input
    
    Input format:
    {
        "data": [
            {
                "server_id": 638939,
                "service_description": "CPU_Usage",
                "hour": 10,
                "day_of_week": 2,
                "is_weekend": 0,
                "is_working_hour": 1,
                "season": "Autumn",
                "cpu_lag_1": 45.5,
                "cpu_lag_2": 43.2,
                "cpu_lag_3": 42.8,
                "time_gap_minutes": 30.0
            }
        ]
    }
    """
    try:
        data = json.loads(raw_data)
        
        # Convert input to DataFrame
        df = pd.DataFrame(data["data"])
        
        # Prepare features for model
        features = [
            "cpu_lag_1", "cpu_lag_2", "cpu_lag_3",
            "time_gap_minutes", "hour", "day_of_week",
            "is_weekend", "is_working_hour", "season",
            "service_description"
        ]
        
        X = df[features]
        
        # Make predictions
        predictions = model.predict(X)
        
        # Format response
        results = {
            "predictions": predictions.tolist(),
            "input_count": len(df),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return json.dumps(results)
    
    except Exception as e:
        return json.dumps({"error": str(e)})
