"""
Register XGBoost Model in Azure ML
"""

from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure_config import get_ml_client, MODEL_NAME, MODEL_VERSION


def register_model():
    """
    Register the trained XGBoost model to Azure ML
    """
    client = get_ml_client()
    
    print(f"Registering model: {MODEL_NAME} (version {MODEL_VERSION})")
    
    # Register model
    model = Model(
        path="../xgboost_cpu_forecaster.pkl",  # Path to your saved model
        name=MODEL_NAME,
        version=MODEL_VERSION,
        type=AssetTypes.CUSTOM_MODEL,
        description="XGBoost model for CPU usage forecasting (14-day ahead)",
        properties={
            "model_type": "xgboost",
            "task": "time_series_forecasting",
            "input_features": "cpu_lag_1, cpu_lag_2, cpu_lag_3, time_gap_minutes, hour, day_of_week, is_weekend, is_working_hour, season, service_description",
            "output": "predicted_CPU_percent",
            "training_data": "CPU historical usage",
            "metrics": "MAE, RMSE, R2"
        }
    )
    
    registered_model = client.models.create_or_update(model)
    
    print(f"✅ Model registered successfully!")
    print(f"   Name: {registered_model.name}")
    print(f"   Version: {registered_model.version}")
    print(f"   ID: {registered_model.id}")
    
    return registered_model


if __name__ == "__main__":
    register_model()
