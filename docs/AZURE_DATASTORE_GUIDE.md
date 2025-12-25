# 🗂️ Azure ML Datastore Guide

## What You Did (Smart Move!)

You registered your data as an **Azure ML Data Source**. This is the **correct way** to work with data in Azure ML! 

When you upload data to Azure ML:
- It's stored in the **workspace blob storage** (called a datastore)
- You can create **datasets** that reference this data
- Your scripts can access it using special URIs

---

## 📍 Where Is Your Data?

Your data is now in one of these places:

### Option 1: Datastore (Raw Files)
```
azureml://datastores/workspaceblobstore/paths/<your-folder>/
```

### Option 2: Dataset (Registered Data Asset)
```
azureml://subscriptions/<sub-id>/resourcegroups/<rg>/workspaces/<ws>/data/<dataset-name>/<version>
```

---

## 🔍 How to Find Your Data Path

### Method 1: Azure ML Studio UI
1. Go to https://ml.azure.com
2. Select workspace: `cpu-project`
3. Click **"Data"** in left menu
4. You'll see your registered datasets
5. Click on your dataset → **"Consume"** tab
6. Copy the data path shown

### Method 2: From Compute Instance
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Connect to workspace
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="3c903801-0878-49d9-9d2c-3ed7f0e0ad1c",
    resource_group_name="RG_JIT02",
    workspace_name="cpu-project"
)

# List all datasets
for data_asset in ml_client.data.list():
    print(f"Name: {data_asset.name}, Version: {data_asset.version}")
    print(f"Path: {data_asset.path}")
```

---

## 📂 Working with Your Data on Compute Instance

### Setup on Compute Instance

When you create your compute instance and want to work with your registered data:

#### 1. Access Dataset Directly
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import pandas as pd

# Connect (automatic authentication on compute instance)
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="3c903801-0878-49d9-9d2c-3ed7f0e0ad1c",
    resource_group_name="RG_JIT02",
    workspace_name="cpu-project"
)

# Get your dataset (replace with your dataset name)
data_asset = ml_client.data.get(name="cpu_usage_data", version="1")

# Download to compute instance
import os
df = pd.read_csv(data_asset.path)  # Azure ML handles the download
```

#### 2. Upload Model File to Compute Instance

Since you can't find the `xgboost_cpu_forecaster.pkl` file locally, here's what to do:

**Option A: Train on Compute Instance**
```python
# On your compute instance, retrain the model:
import xgboost as xgb
import pandas as pd

# Load your data from datastore
df = pd.read_csv(data_asset.path)

# Train model (your existing code)
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# Save model on compute instance
model.save_model("xgboost_cpu_forecaster.pkl")
```

**Option B: Upload Existing Model**
1. Go to Compute Instance in Azure ML Studio
2. Click "Jupyter" or "VS Code" to open the instance
3. Use the file browser to upload `xgboost_cpu_forecaster.pkl`
4. Or use Azure ML SDK:
```python
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

# Upload and register in one step
model = Model(
    path="/path/on/compute/xgboost_cpu_forecaster.pkl",
    name="xgboost-cpu-forecaster",
    type=AssetTypes.CUSTOM_MODEL,
    description="XGBoost model for CPU usage forecasting"
)

registered_model = ml_client.models.create_or_update(model)
```

---

## 🚀 Complete Workflow on Compute Instance

### Step 1: Create Compute Instance
1. Go to https://ml.azure.com
2. Navigate to **Compute** → **Compute instances**
3. Click **"+ New"**
4. Choose: **Standard_DS3_v2** (4 cores, 14GB RAM)
5. Name it: `cpu-forecaster-dev`
6. Click **Create** (takes 3-5 minutes)

### Step 2: Open Terminal on Compute Instance
1. Once running, click **"Jupyter"** or **"Terminal"**
2. This opens a cloud Linux environment with Azure authentication

### Step 3: Clone Your Code (if using Git)
```bash
git clone <your-repo-url>
cd CPU_challenge/deploy
```

### Step 4: Install Dependencies
```bash
pip install -r config/requirements.txt
```

### Step 5: Work with Your Data
```python
# data_access.py - Run this first to test
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import pandas as pd

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="3c903801-0878-49d9-9d2c-3ed7f0e0ad1c",
    resource_group_name="RG_JIT02",
    workspace_name="cpu-project"
)

# List your data assets
print("Available datasets:")
for data in ml_client.data.list():
    print(f"  - {data.name} (v{data.version}): {data.path}")

# Load your specific dataset (replace name/version)
data_asset = ml_client.data.get(name="your-dataset-name", version="1")
df = pd.read_csv(data_asset.path)
print(f"\nLoaded {len(df)} rows")
```

### Step 6: Register Your Model
```bash
# Make sure model file exists on compute instance
python azure_ml/register_model.py xgboost_cpu_forecaster.pkl
```

### Step 7: Deploy
```bash
python azure_ml/deploy_endpoint.py
```

---

## 🎯 Quick Reference Commands

### Check Connection
```bash
python azure_ml/azure_config.py
```

### List Data Assets
```bash
az ml data list --resource-group RG_JIT02 --workspace-name cpu-project
```

### Upload File to Datastore
```bash
az ml datastore upload \
  --name workspaceblobstore \
  --src-path ./xgboost_cpu_forecaster.pkl \
  --target-path models/ \
  --resource-group RG_JIT02 \
  --workspace-name cpu-project
```

### Download from Datastore
```bash
az ml datastore download \
  --name workspaceblobstore \
  --target-path . \
  --prefix models/xgboost_cpu_forecaster.pkl \
  --resource-group RG_JIT02 \
  --workspace-name cpu-project
```

---

## 🔧 Updated Scripts

Your `register_model.py` is now updated to accept a model path:

```python
# Default - looks for model in current directory
python azure_ml/register_model.py

# Custom path - specify where your model is
python azure_ml/register_model.py ./models/xgboost_cpu_forecaster.pkl
python azure_ml/register_model.py /mnt/batch/tasks/.../model.pkl
```

---

## 💡 Best Practices

### ✅ DO:
- Work from compute instance (automatic auth, no local issues)
- Register data as datasets (versioning, lineage tracking)
- Use datastore URIs in scripts (`azureml://...`)
- Keep model files in datastores or compute instance storage

### ❌ DON'T:
- Don't use local file paths (`../model.pkl`) in Azure scripts
- Don't try to authenticate locally if you have MFA issues
- Don't download large datasets to local machine

---

## 🆘 Troubleshooting

### "Can't find my dataset"
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="3c903801-0878-49d9-9d2c-3ed7f0e0ad1c",
    resource_group_name="RG_JIT02",
    workspace_name="cpu-project"
)

# List everything
for data in ml_client.data.list():
    print(f"{data.name} v{data.version}")
```

### "Model file doesn't exist"
**Solution:** Upload it to compute instance or datastore first

**Upload to datastore:**
```bash
az ml datastore upload \
  --name workspaceblobstore \
  --src-path ./xgboost_cpu_forecaster.pkl \
  --target-path models/
```

**Then reference it:**
```python
python azure_ml/register_model.py azureml://datastores/workspaceblobstore/paths/models/xgboost_cpu_forecaster.pkl
```

### "Authentication failed"
**Solution:** Use compute instance - it has automatic authentication. No `az login` needed!

---

## 📞 Next Steps

1. **Create compute instance** (if not done)
   - Go to https://ml.azure.com → Compute → New
   
2. **Find your dataset name**
   - Go to Data tab in Azure ML Studio
   - Note the exact name and version
   
3. **Upload model file**
   - Use Jupyter file browser on compute instance
   - Or retrain model on compute instance
   
4. **Run deployment**
   - All scripts work automatically on compute instance
   - No authentication issues!

---

**🎉 You're using Azure ML the right way! Data sources/datastores are the proper approach.**
