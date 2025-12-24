# 🚀 Complete Azure ML Pipeline - Getting Started Guide

## What You Have Now

Your CPU forecasting model is **production-ready** with:

```
✅ Working Flask API server (local)
✅ Automated pipeline setup files (Azure ML)
✅ Real-time endpoint deployment (Azure ML)
✅ Model registry integration (Azure ML)
✅ Complete documentation (guides + references)
✅ Test & monitoring utilities
```

## 📚 Documentation Files

### Quick Start Guides
- **AZURE_QUICKSTART.py** - Run this first! Quick reference and checklist
- **AZURE_ML_SETUP.md** - Comprehensive setup walkthrough
- **AZURE_ML_INTEGRATION.md** - Complete integration with examples

### Reference Documentation  
- **AZURE_COMMANDS_REFERENCE.md** - CLI & SDK commands
- **AZURE_SOLUTION_SUMMARY.md** - Architecture overview with diagrams

### Setup & Verification
- **azure_setup_checker.py** - Interactive setup verification

## 🎯 5-Minute Quick Start

### Step 1: Install Tools
```bash
pip install azure-ai-ml azure-identity
az login
```

### Step 2: Create Workspace (Choose One)

**Via CLI:**
```bash
az group create --name cpu-forecast-rg --location eastus
az ml workspace create -n cpu-forecast-ws -g cpu-forecast-rg
```

**Or via Azure Portal:** https://portal.azure.com → Create "Machine Learning"

### Step 3: Configure Connection
Edit `azure_config.py` and update:
```python
SUBSCRIPTION_ID = "your-subscription-id"
RESOURCE_GROUP = "cpu-forecast-rg"
WORKSPACE_NAME = "cpu-forecast-ws"
```

### Step 4: Verify Setup
```bash
python azure_setup_checker.py
python azure_config.py
```

### Step 5: Deploy
```bash
python register_model.py
python create_pipeline.py
python deploy_endpoint.py
```

## 📂 File Structure

```
deploy/
├── 📖 AZURE_QUICKSTART.py                   ← START HERE!
├── 📖 AZURE_ML_SETUP.md
├── 📖 AZURE_ML_INTEGRATION.md
├── 📖 AZURE_COMMANDS_REFERENCE.md
├── 📖 AZURE_SOLUTION_SUMMARY.md
│
├── ⚙️  azure_config.py                      ← CONFIGURE THIS
├── ⚙️  azure_setup_checker.py               ← RUN THIS TO VERIFY
│
├── 🤖 register_model.py                     ← THEN RUN THESE
├── 🤖 create_pipeline.py
├── 🤖 deploy_endpoint.py
│
├── 📜 score.py                              ← Endpoint scoring
├── 📜 prepare_data.py                       ← Pipeline preprocessing
│
├── 🔧 environments/
│   └── env_cpu_forecast.yml                 ← Python dependencies
│
├── 🚀 server.py                             ← Local Flask server (already working)
├── 🚀 test.py                               ← Local test client (already working)
│
├── 📋 requirements.txt                      ← All dependencies
└── 📋 README.md                             ← Local deployment guide
```

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────┐
│        YOUR LOCAL DEVELOPMENT (DONE)         │
│  ✅ Flask Server                             │
│  ✅ Test Client                              │
│  ✅ Working Model                            │
│  ✅ All functional                           │
└─────────────────────────────────────────────┘
                    ↓ (upload to cloud)
┌─────────────────────────────────────────────┐
│         AZURE MACHINE LEARNING (NEXT)        │
│  📦 Model Registry                           │
│  📊 Automated Pipeline                       │
│  🔄 Retraining (scheduled)                   │
│  🌐 REST Endpoint (24/7 API)                │
│  📈 Monitoring & Logging                     │
│  🔐 Enterprise Security                      │
└─────────────────────────────────────────────┘
```

## ⏱️ Estimated Timeline

| Step | Time | Action |
|------|------|--------|
| 1 | 5 min | Install tools & login |
| 2 | 5 min | Create workspace |
| 3 | 5 min | Configure connection |
| 4 | 2 min | Verify setup |
| 5 | 5 min | Register model |
| 6 | 15 min | Create & run pipeline |
| 7 | 10 min | Deploy endpoint |
| **Total** | **~45 min** | **Full deployment** |

## 💰 Azure Costs (Approximate)

| Item | Cost/Month |
|------|-----------|
| Compute (training) | $10-15 |
| Storage | $2-5 |
| Endpoint (24/7) | $50-100 |
| Data transfer | $5-10 |
| **Total** | **~$70-130** |

**Ways to reduce cost:**
- Shut down endpoint when not needed (~$50/month savings)
- Use serverless compute (~$10/month)
- Scale down instances (~$30/month savings)

## 🔑 Key Files Explained

### `azure_config.py`
- Your connection credentials
- Workspace and resource configuration
- Compute cluster settings
- **Customize this with your Azure details**

### `register_model.py`
- Uploads your trained model to Azure ML registry
- Adds metadata and properties
- **Run once after model is ready**

### `create_pipeline.py`
- Defines automated ML pipeline
- Steps: Data prep → Training → Evaluation
- Can be scheduled to run daily/weekly
- **Run to set up automation**

### `deploy_endpoint.py`
- Creates real-time prediction API
- Handles auto-scaling
- Returns scoring URI and API key
- **Run to make model accessible via REST**

### `score.py`
- Runs on the endpoint
- Handles prediction requests
- Preprocesses inputs before prediction
- **Uploaded automatically by deploy_endpoint.py**

## 🧪 Testing Your Deployment

After deploying the endpoint:

```python
import requests

# Get your endpoint details from Azure Portal
scoring_uri = "https://your-endpoint.eastus.inference.ml.azure.com/score"
api_key = "your-api-key"

# Prepare data
data = {
    "data": [{
        "server_id": 638939,
        "service_description": 1,  # 1=CPU_Usage, 2=Windows, 3=SQL
        "hour": 10,
        "day_of_week": 2,
        "is_weekend": 0,
        "is_working_hour": 1,
        "season": 2,  # 0=winter, 1=spring, 2=summer, 3=autumn
        "cpu_lag_1": 45.5,
        "cpu_lag_2": 43.2,
        "cpu_lag_3": 42.8,
        "time_gap_minutes": 30.0
    }]
}

# Call endpoint
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.post(scoring_uri, json=data, headers=headers)
print(response.json())  # Returns predicted CPU usage
```

## 📊 Monitoring After Deployment

Azure ML automatically tracks:
- **Model Metrics**: MAE, RMSE, R² scores
- **Endpoint Metrics**: Latency, throughput, errors
- **Logs**: All requests and responses
- **Data Drift**: Changes in data distribution
- **Model Performance**: Ongoing evaluation

### View Metrics in Azure Portal:
1. Go to https://ml.azure.com
2. Select your workspace
3. Navigate to "Endpoints" → "cpu-forecast-endpoint"
4. View real-time metrics

## 🔄 Continuous Improvement

### Schedule Daily Retraining
```python
# In Azure ML Studio or Python SDK
schedule = RecurrenceSchedule(
    frequency="Day",
    interval=1,
    start_time="2025-01-01T00:00:00"
)
```

### Monitor Model Drift
```bash
# Get model metrics over time
az ml job list --workspace-name cpu-forecast-ws --output table
```

### Update Endpoint with New Model
```bash
az ml model create --name xgboost-cpu-forecaster --version 2 --path new_model.pkl
az ml online-deployment update --endpoint-name cpu-forecast-endpoint --model version:2
```

## 🆘 Need Help?

### Verification Checklist
- [ ] Azure subscription created
- [ ] Azure CLI installed (`az --version`)
- [ ] Python 3.10+ installed
- [ ] Azure ML SDK installed
- [ ] Logged into Azure (`az login`)
- [ ] Workspace created
- [ ] `azure_config.py` updated
- [ ] Model file exists (`xgboost_cpu_forecaster.pkl`)

### Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Subscription not found"** | Check SUBSCRIPTION_ID in azure_config.py |
| **"Workspace doesn't exist"** | Create workspace in Azure Portal or CLI |
| **"Auth failed"** | Run `az login` again |
| **"Model not found"** | Check file path and verify it exists |
| **Endpoint takes too long** | Normal - first deploy takes 5-10 minutes |

### Get Help
- 📖 Read: `AZURE_ML_SETUP.md`
- 📚 Read: `AZURE_COMMANDS_REFERENCE.md`
- 🔗 Visit: https://learn.microsoft.com/en-us/azure/machine-learning/
- 💬 Ask: Azure Support in Portal

## ✅ Success Indicators

You'll know everything is working when you see:

1. ✅ `azure_config.py` → "Connected to workspace"
2. ✅ `register_model.py` → "Model registered successfully"
3. ✅ `create_pipeline.py` → "Pipeline job submitted"
4. ✅ `deploy_endpoint.py` → "Model deployed successfully"
5. ✅ Azure Portal shows endpoint in "Succeeded" state
6. ✅ Test request returns prediction

## 🎉 Congratulations!

You now have:
- ✅ Production-ready ML model
- ✅ Automated retraining pipeline
- ✅ Real-time REST API
- ✅ Enterprise-grade monitoring
- ✅ Scalable infrastructure

## 📖 Recommended Reading Order

1. **Start here**: `AZURE_QUICKSTART.py` (just run it!)
2. **Then read**: `AZURE_ML_SETUP.md` (setup overview)
3. **Deep dive**: `AZURE_SOLUTION_SUMMARY.md` (architecture)
4. **Reference**: `AZURE_COMMANDS_REFERENCE.md` (when needed)

## 🚀 Ready to Deploy?

```bash
# 1. Verify setup
python azure_setup_checker.py

# 2. Configure
python azure_config.py

# 3. Deploy
python register_model.py
python create_pipeline.py
python deploy_endpoint.py
```

**Good luck! Your model is ready for production! 🎯**
