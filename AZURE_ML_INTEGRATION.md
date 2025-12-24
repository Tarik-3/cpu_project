# Azure ML Pipeline Integration - Complete Guide

## 📋 Overview

Your CPU forecasting model is now ready for Azure ML. Here's a complete guide to deploy it to production.

## 🎯 What You'll Have

After following these steps:
- ✅ Model registered in Azure ML
- ✅ Automated ML pipeline (data prep → training → evaluation)
- ✅ Real-time prediction API endpoint
- ✅ Auto-scaling infrastructure
- ✅ Full monitoring and logging

## 📦 New Files Created

```
deploy/
├── AZURE_ML_SETUP.md              ← Detailed setup documentation
├── AZURE_QUICKSTART.py            ← Quick reference guide
├── azure_config.py                ← Azure connection & configuration
├── register_model.py              ← Upload model to Azure ML
├── create_pipeline.py             ← Define ML pipeline
├── deploy_endpoint.py             ← Deploy real-time endpoint
├── score.py                       ← Endpoint scoring script
├── prepare_data.py                ← Data preprocessing step
└── environments/
    └── env_cpu_forecast.yml       ← Python dependencies
```

## 🚀 Quick Start (5 Steps)

### Step 1: Install Tools
```bash
pip install azure-ai-ml azure-identity
az login
```

### Step 2: Create Workspace (Azure Portal or CLI)
```bash
az group create --name cpu-forecast-rg --location eastus
az ml workspace create -n cpu-forecast-ws -g cpu-forecast-rg
```

### Step 3: Configure Connection
Edit `azure_config.py`:
```python
SUBSCRIPTION_ID = "your-subscription-id"
RESOURCE_GROUP = "cpu-forecast-rg"
WORKSPACE_NAME = "cpu-forecast-ws"
```

Verify:
```bash
python azure_config.py
```

### Step 4: Register & Deploy
```bash
python register_model.py
python create_pipeline.py
python deploy_endpoint.py
```

### Step 5: Test Endpoint
```bash
python deploy_endpoint.py  # Tests automatically at end
```

## 🔄 Azure ML Pipeline Architecture

```
RAW DATA (data.csv)
        ↓
    [Prepare Data Step]
    - Encode categories
    - Create lag features
    - Handle missing values
        ↓
    [Training Step]
    - Split train/test
    - Train XGBoost
    - Save model
        ↓
    [Evaluation Step]
    - Calculate MAE, RMSE, R²
    - Log metrics
    - Register model
        ↓
    [Deploy Step]
    - Create endpoint
    - Enable auto-scaling
    - Ready for predictions
```

## 📊 Monitored Metrics

Azure ML automatically tracks:
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**
- **Execution time**
- **Endpoint latency**
- **Model drift**
- **Prediction volume**

## 🌐 REST Endpoint

Once deployed, your model is accessible via HTTP:

```python
import requests
import json

# Endpoint details (from Azure Portal)
scoring_uri = "https://your-endpoint.eastus.inference.ml.azure.com/score"
key = "your-api-key"

# Prepare data
data = {
    "data": [
        {
            "server_id": 638939,
            "service_description": 1,
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
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

response = requests.post(scoring_uri, json=data, headers=headers)
print(response.json())
```

## 💰 Cost Breakdown

| Component | Monthly Cost |
|-----------|--------------|
| Compute (8h/week) | $10-20 |
| Storage | $2-5 |
| Endpoint (24/7) | $50-100 |
| Data transfer | $5-10 |
| **Total** | **~$70-150** |

💡 **Cost optimization tips:**
- Use serverless compute for training (pay-per-use)
- Auto-scale endpoint from 0-2 instances
- Delete unused endpoints and models
- Use spot instances for non-critical jobs

## 🔒 Security Best Practices

1. **Authentication**
   ```bash
   az login  # Always use managed identity
   ```

2. **Key Management**
   - Store keys in Azure Key Vault
   - Rotate keys regularly
   - Never commit keys to git

3. **Network Security**
   - Enable private endpoints
   - Use VNet integration
   - Configure NSGs

4. **Data Security**
   - Enable data encryption at rest
   - Use HTTPS only
   - Enable audit logging

## 📈 Monitoring & Alerting

### Azure Portal Dashboard
- Go to https://ml.azure.com
- Select your workspace
- View real-time metrics

### Set Up Alerts
```python
# In Azure Portal:
# Monitor → Alerts → New alert rule
# - Resource: Your endpoint
# - Condition: CPU > 80% or Latency > 1000ms
# - Action: Send email/SMS
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Auth fails | `az login` and verify subscription ID |
| Quota exceeded | Increase compute quota in Azure Portal |
| Endpoint 500 error | Check logs: `client.jobs.stream(job_name)` |
| Slow predictions | Check instance size, scale up if needed |
| High costs | Reduce endpoint instances, use serverless compute |

## 📚 Next Steps

1. **Monitor in Production**
   - Check endpoint metrics daily
   - Track prediction latency
   - Monitor model drift

2. **Retrain Regularly**
   - Schedule pipeline to run weekly
   - Collect new data
   - Evaluate model performance

3. **Improve Model**
   - Experiment with hyperparameters
   - Try different algorithms
   - Add new features

4. **Scale Up**
   - Add batch prediction for large datasets
   - Implement feature store
   - Connect to data pipeline

## 📞 Support Resources

- **Azure ML Docs**: https://learn.microsoft.com/en-us/azure/machine-learning/
- **Python SDK**: https://aka.ms/aml-sdk
- **Code Examples**: https://github.com/Azure/azureml-examples
- **Community Forum**: https://github.com/Azure/MachineLearningNotebooks/discussions

## ✅ Deployment Checklist

- [ ] Azure subscription created
- [ ] Azure CLI installed
- [ ] Azure ML workspace created
- [ ] `azure_config.py` updated with your details
- [ ] Model registered in Azure ML
- [ ] Pipeline created and ran successfully
- [ ] Endpoint deployed
- [ ] Endpoint tested successfully
- [ ] Alerts configured
- [ ] Team trained on monitoring

## 🎉 You're Ready!

Your ML model is now in production on Azure ML with:
- ✅ Automated retraining pipeline
- ✅ Real-time REST API
- ✅ Auto-scaling infrastructure
- ✅ Full monitoring & logging
- ✅ Enterprise-grade security

**Next**: Set up continuous retraining by scheduling the pipeline to run weekly!
