# Azure ML Pipeline Setup Guide

This guide walks through creating an Azure ML Pipeline for the CPU Usage Forecasting Model.

## Prerequisites

1. **Azure Subscription** - Create at https://portal.azure.com
2. **Azure ML Workspace** - Create in Azure Portal
3. **Install Azure ML SDK**:
   ```bash
   pip install azure-ai-ml azure-identity
   ```

## Step 1: Create an Azure ML Workspace

### Using Azure Portal:
1. Go to portal.azure.com
2. Create a new **Machine Learning** resource
3. Fill in:
   - **Resource group**: Create new (e.g., `cpu-forecast-rg`)
   - **Workspace name**: e.g., `cpu-forecast-ws`
   - **Region**: Choose closest to you
4. Review + Create

### Or Using Azure CLI:
```bash
az group create --name cpu-forecast-rg --location eastus
az ml workspace create -n cpu-forecast-ws -g cpu-forecast-rg
```

## Step 2: Prepare Your Environment

### Create `azure_config.py`:
```python
import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Configuration
SUBSCRIPTION_ID = "your-subscription-id"
RESOURCE_GROUP = "cpu-forecast-rg"
WORKSPACE_NAME = "cpu-forecast-ws"

def get_ml_client():
    """Get authenticated ML client"""
    credential = DefaultAzureCredential()
    return MLClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP,
        workspace_name=WORKSPACE_NAME
    )
```

### Find Your IDs:
```bash
# List subscriptions
az account list --output table

# List resource groups
az group list --output table

# List workspaces
az ml workspace list -g cpu-forecast-rg --output table
```

## Step 3: Register Your Model

See `register_model.py` for code to upload model to Azure ML.

## Step 4: Create Pipeline

See `create_pipeline.py` for the complete pipeline implementation.

## Step 5: Run the Pipeline

```python
from azure.ai.ml import dsl

# Get client
client = get_ml_client()

# Submit job
returned_job = client.jobs.create_or_update(pipeline_job)

# Monitor progress
client.jobs.stream(returned_job.name)
```

## Step 6: Deploy as Real-time Endpoint

See `deploy_endpoint.py` for endpoint deployment code.

## Step 7: Test the Endpoint

```python
import json
import requests

# Get endpoint details
endpoint = client.online_endpoints.get("cpu-forecast-endpoint")
scoring_uri = endpoint.scoring_uri
key = client.online_endpoints.get_keys("cpu-forecast-endpoint").primary_key

# Prepare test data
test_data = {
    "data": [
        {
            "server_id": 638939,
            "service_description": "CPU_Usage",
            "hour": 10,
            "day_of_week": 2,
            "is_weekend": 0,
            "is_working_hour": 1,
            "season": 2,
            "cpu_lag_1": 45.5,
            "cpu_lag_2": 43.2,
            "cpu_lag_3": 42.8,
            "time_gap_minutes": 30.0
        }
    ]
}

# Call endpoint
headers = {"Content-Type": "application/json"}
headers["Authorization"] = f"Bearer {key}"

response = requests.post(scoring_uri, json=test_data, headers=headers)
print(response.json())
```

## Azure ML Pipeline Components

### 1. **Data Preparation Step**
- Load raw CSV
- Preprocess (encode, create lags)
- Train/Test split

### 2. **Training Step**
- Load preprocessed data
- Train XGBoost model
- Evaluate metrics

### 3. **Evaluation Step**
- Calculate MAE, RMSE, R²
- Compare with baseline
- Log metrics

### 4. **Model Registration**
- Register trained model
- Store in Azure ML registry

### 5. **Deployment Step**
- Create inference environment
- Deploy to real-time endpoint

## File Structure

```
deploy/
├── azure_config.py           # Azure credentials & setup
├── register_model.py         # Upload model to Azure ML
├── create_pipeline.py        # Define and run pipeline
├── deploy_endpoint.py        # Deploy real-time endpoint
├── test_endpoint.py          # Test deployed endpoint
├── environments/
│   └── env_cpu_forecast.yml # Conda environment file
└── score.py                  # Scoring script for endpoint
```

## Key Azure ML Concepts

### **Environments**
- Define package dependencies
- Specify Python version
- Ensure consistency across pipeline

### **Compute Targets**
- `compute-cluster`: For training/processing
- `compute-instance`: For development
- Serverless: Pay-per-use

### **Data Assets**
- Version your data
- Track lineage
- Manage datasets

### **Pipelines**
- Automated workflows
- Step dependencies
- Reproducible ML

### **Endpoints**
- Real-time: Low-latency predictions
- Batch: Process large data
- Auto-scaling available

## Monitoring & Logging

Azure ML automatically tracks:
- ✅ Metrics (MAE, RMSE, R²)
- ✅ Logs (stdout/stderr)
- ✅ Data lineage
- ✅ Model versions
- ✅ Prediction latency

## Cost Estimation

**Monthly costs (approximate)**:
- Compute (8 hours): $10-30
- Storage: $2-5
- Endpoint: $50-100
- Data transfer: varies

## Next Steps

1. ✅ Create workspace (5 minutes)
2. ✅ Register model (1 minute)
3. ✅ Create pipeline (5 minutes)
4. ✅ Run pipeline (10-15 minutes)
5. ✅ Deploy endpoint (5 minutes)
6. ✅ Test predictions (2 minutes)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Check subscription ID and credentials |
| Quota exceeded | Increase compute quota in Azure Portal |
| Package not found | Update requirements in conda YAML |
| Timeout errors | Increase timeout in pipeline step |
| Endpoint 500 error | Check logs in Azure Portal |

## Useful Links

- [Azure ML Docs](https://learn.microsoft.com/en-us/azure/machine-learning/)
- [Python SDK](https://aka.ms/aml-sdk)
- [Pipeline Examples](https://github.com/Azure/azureml-examples)
- [Cost Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
