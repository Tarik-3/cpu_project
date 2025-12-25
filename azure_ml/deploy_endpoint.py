"""
Deploy model as real-time endpoint
"""

from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration
)
from azure_config import (
    get_ml_client, MODEL_NAME, MODEL_VERSION,
    ENDPOINT_NAME, LOCATION
)


def create_endpoint():
    """Create online endpoint for real-time predictions"""
    
    client = get_ml_client()
    
    print(f"Creating endpoint: {ENDPOINT_NAME}")
    
    # Create endpoint
    endpoint = ManagedOnlineEndpoint(
        name=ENDPOINT_NAME,
        description="Real-time CPU forecasting endpoint",
        auth_mode="key",
        location=LOCATION,
        tags={
            "model": "xgboost",
            "task": "forecasting",
            "version": MODEL_VERSION
        }
    )
    
    client.online_endpoints.begin_create_or_update(endpoint).result()
    print(f"✅ Endpoint created: {ENDPOINT_NAME}")
    
    return endpoint


def deploy_model():
    """Deploy model to endpoint"""
    
    client = get_ml_client()
    
    print(f"Deploying model to endpoint...")
    
    # Get registered model
    model = client.models.get(MODEL_NAME, MODEL_VERSION)
    
    # Create environment
    env = Environment(
        conda_file="environments/env_cpu_forecast.yml",
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04"
    )
    env = client.environments.create_or_update(env)
    
    # Create deployment
    deployment = ManagedOnlineDeployment(
        name="cpu-forecast-deployment",
        endpoint_name=ENDPOINT_NAME,
        model=model,
        environment=env,
        code_configuration=CodeConfiguration(
            code=".",
            scoring_script="score.py"
        ),
        instance_type="Standard_DS2_v2",
        instance_count=1,
        request_settings={
            "request_timeout_ms": 3000,
            "max_concurrent_requests_per_instance": 1,
        },
        liveness_probe={
            "failure_threshold": 30,
            "success_threshold": 1,
            "timeout": 2,
            "period": 10,
            "initial_delay": 10,
        }
    )
    
    # Deploy
    client.online_deployments.begin_create_or_update(deployment).result()
    
    # Set as default deployment
    endpoint = client.online_endpoints.get(ENDPOINT_NAME)
    endpoint.traffic = {"cpu-forecast-deployment": 100}
    client.online_endpoints.begin_create_or_update(endpoint).result()
    
    print(f"✅ Model deployed successfully!")
    
    # Get endpoint details
    endpoint = client.online_endpoints.get(ENDPOINT_NAME)
    print(f"\n📋 Endpoint Details:")
    print(f"   Name: {endpoint.name}")
    print(f"   Scoring URI: {endpoint.scoring_uri}")
    print(f"   State: {endpoint.provisioning_state}")
    
    return endpoint


def test_endpoint():
    """Test the deployed endpoint"""
    
    client = get_ml_client()
    
    import json
    import requests
    
    # Get endpoint
    endpoint = client.online_endpoints.get(ENDPOINT_NAME)
    scoring_uri = endpoint.scoring_uri
    
    # Get key
    keys = client.online_endpoints.get_keys(ENDPOINT_NAME)
    key = keys.primary_key
    
    # Test data
    test_data = {
        "data": [
            {
                "server_id": 638939,
                "service_description": 1,  # CPU_Usage
                "hour": 10,
                "day_of_week": 2,
                "is_weekend": 0,
                "is_working_hour": 1,
                "season": 2,  # Summer
                "cpu_lag_1": 45.5,
                "cpu_lag_2": 43.2,
                "cpu_lag_3": 42.8,
                "time_gap_minutes": 30.0
            }
        ]
    }
    
    # Call endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    
    print(f"\n🧪 Testing endpoint...")
    response = requests.post(scoring_uri, json=test_data, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Prediction successful!")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Message: {response.text}")
    
    return response


if __name__ == "__main__":
    # Create endpoint
    create_endpoint()
    
    # Deploy model
    deploy_model()
    
    # Test endpoint
    # test_endpoint()  # Uncomment to test
