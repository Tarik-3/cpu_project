"""
Register XGBoost Model in Azure ML
"""

from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure_config import get_ml_client, MODEL_NAME, MODEL_VERSION


def register_model(model_path="xgboost_cpu_forecaster.pkl"):
    """
    Register the trained XGBoost model to Azure ML
    
    Args:
        model_path: Path to model file. On compute instance, use local path.
                   Example: "xgboost_cpu_forecaster.pkl" or "./models/model.pkl"
    """
    client = get_ml_client()
    
    print(f"Registering model: {MODEL_NAME} (version {MODEL_VERSION})")
    print(f"Model path: {model_path}")
    
    # Register model
    model = Model(
        path=model_path,  # Path to your saved model on compute instance
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
    import sys
    
    # Allow model path as command line argument
    model_path = sys.argv[1] if len(sys.argv) > 1 else "xgboost_cpu_forecaster.pkl"
    
    print(f"\nℹ️  Using model file: {model_path}")
    register_model(model_path)
    print("\n✅ Model registration completed!")

