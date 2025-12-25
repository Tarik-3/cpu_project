# Azure Data Access Solutions

You have 3 options to access your Azure ML data:

## 🔥 Quick Solution: Generate SAS Token (Recommended for Testing)

### Step 1: Go to Azure Portal
1. Open https://portal.azure.com
2. Navigate to **Storage Accounts**
3. Find your storage account: `cpuproject9177426007`
4. Click on it

### Step 2: Generate SAS Token
1. In left menu, click **Shared access signature**
2. Set permissions:
   - ✅ **Read**
   - ✅ **List**
   - ⬜ Write (not needed)
3. Set expiry date: Choose 1 day or 1 week
4. Click **Generate SAS and connection string**
5. Copy the **Blob service SAS URL**

### Step 3: Build Full URL
Combine:
```
Base URL: https://cpuproject9177426007.blob.core.windows.net
Container: azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4
Path: UI/2025-12-24_111626_UTC/server_forecastability_scores.csv
SAS Token: ?sv=2022-11-02&ss=b&srt=sco&sp=rwdlac&se=...
```

**Full URL:**
```
https://cpuproject9177426007.blob.core.windows.net/azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4/UI/2025-12-24_111626_UTC/server_forecastability_scores.csv?sv=2022-11-02&ss=b&srt=sco&sp=rwdlac&se=...
```

### Step 4: Use in test_with_sas.py
```python
AZURE_BLOB_URL_WITH_SAS = "https://cpuproject9177426007.blob.core.windows.net/azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4/UI/2025-12-24_111626_UTC/server_forecastability_scores.csv?sv=YOUR-SAS-TOKEN"
```

### Step 5: Run
```powershell
cd deploy
python test_with_sas.py
```

---

## 🔐 Solution 2: Use Azure ML SDK (Most Secure)

### Prerequisites
```powershell
# Install required packages
pip install azure-ai-ml azure-identity azure-storage-blob

# Login to Azure
az login
```

### Update azure_config.py
1. Get your subscription ID:
```powershell
az account show --query id --output tsv
```

2. Edit `azure_config.py`:
```python
SUBSCRIPTION_ID = "your-actual-subscription-id"
RESOURCE_GROUP = "your-resource-group-name"  
WORKSPACE_NAME = "your-workspace-name"
```

### Run test_azure_data.py
```powershell
python test_azure_data.py
```

This uses proper Azure authentication and is recommended for production.

---

## 📂 Solution 3: Download File Locally (Simplest)

### Option A: Download from Azure Portal
1. Go to Azure Portal > Storage Accounts
2. Navigate to: `cpuproject9177426007` 
3. Click **Containers** > `azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4`
4. Navigate to: `UI/2025-12-24_111626_UTC/`
5. Click on `server_forecastability_scores.csv`
6. Click **Download**
7. Move to `deploy/` folder

### Option B: Use Azure Storage Explorer
1. Download: https://azure.microsoft.com/features/storage-explorer/
2. Connect to your Azure account
3. Navigate to storage account
4. Download the file

### Option C: Use Azure CLI
```powershell
az storage blob download \
  --account-name cpuproject9177426007 \
  --container-name azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4 \
  --name UI/2025-12-24_111626_UTC/server_forecastability_scores.csv \
  --file deploy/server_forecastability_scores.csv \
  --auth-mode login
```

### Then use test.py
```powershell
# Edit test.py - change DATA_FILE to:
DATA_FILE = "server_forecastability_scores.csv"

# Run
python test.py
```

---

## 🎯 Which Solution to Use?

| Solution | Speed | Security | Best For |
|----------|-------|----------|----------|
| **SAS Token** | ⚡ Fast (2 min) | ⚠️ Expires | Quick testing |
| **Azure SDK** | ⏱️ Medium (10 min) | ✅ Secure | Production |
| **Download File** | ⚡ Fast (1 min) | ✅ Secure | Development |

### My Recommendation:
1. **For immediate testing:** Use SAS token (`test_with_sas.py`)
2. **For production:** Use Azure SDK (`test_azure_data.py`)
3. **For development:** Download file locally (`test.py`)

---

## 📝 Test Files Overview

| File | Purpose | Data Source | Auth Required |
|------|---------|-------------|---------------|
| `test.py` | Original test | Local CSV | No |
| `test_with_sas.py` | Azure with SAS | Azure Blob (SAS) | SAS token only |
| `test_azure_data.py` | Azure with SDK | Azure ML | Full Azure auth |

---

## ❌ Error: "Public access is not permitted"

**This error means:**
Your storage account has public access disabled (good for security!). You need authentication.

**Solutions:**
1. ✅ Use SAS token (temporary key)
2. ✅ Use Azure CLI/SDK authentication
3. ⬜ Enable public access (NOT recommended for production)

---

## 🔧 Troubleshooting

### "Authentication failed"
```powershell
# Re-login to Azure
az login
az account list --output table
az account set --subscription "YOUR-SUBSCRIPTION-ID"
```

### "Subscription not found"
Update `azure_config.py` with correct subscription ID from:
```powershell
az account show
```

### "Storage account not found"
Verify storage account name:
```powershell
az storage account list --output table
```

### "Container not found"
List containers:
```powershell
az storage container list --account-name cpuproject9177426007 --auth-mode login
```

---

## 📞 Quick Help

**Current Azure Storage Account:** `cpuproject9177426007`
**Container:** `azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4`
**File Path:** `UI/2025-12-24_111626_UTC/server_forecastability_scores.csv`

Choose one method above and follow the steps! ✨
