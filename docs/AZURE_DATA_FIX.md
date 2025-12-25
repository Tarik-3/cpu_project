# 🎯 Solution: Accessing Azure ML Data

## Problem
You deployed data to Azure ML and tried to use the blob URL directly in test.py, but got:
```
HTTP Error 409: Public access is not permitted on this storage account
```

## Root Cause
Azure Blob Storage requires authentication. The URL you used doesn't have a SAS token or proper credentials.

## ✅ Solutions (3 Options)

### **Option 1: Use Local File** ⚡ FASTEST (1 minute)
Since `data.csv` already exists in your deploy folder (53MB), just use it:

```powershell
cd deploy
python test.py
```

✅ **Already fixed in test.py** - it now uses local file by default!

---

### **Option 2: Use SAS Token** 🔐 RECOMMENDED FOR TESTING (2 minutes)

1. **Get SAS Token from Azure Portal:**
   - Go to https://portal.azure.com
   - Storage Accounts → `cpuproject9177426007`
   - Left menu → **Shared access signature**
   - Check: Read, List
   - Set expiry: 1 week
   - Click **Generate SAS**
   - Copy the token (starts with `?sv=...`)

2. **Use test_with_sas.py:**
   ```python
   # Edit test_with_sas.py line 15:
   AZURE_BLOB_URL_WITH_SAS = "https://cpuproject9177426007.blob.core.windows.net/azureml-blobstore-6461ea47-a028-4b2b-bcf5-1e1dfee7aad4/UI/2025-12-24_111626_UTC/server_forecastability_scores.csv?sv=YOUR-SAS-TOKEN-HERE"
   ```

3. **Run:**
   ```powershell
   python test_with_sas.py
   ```

---

### **Option 3: Use Azure ML SDK** 🏢 PRODUCTION-READY (10 minutes)

1. **Install packages:**
   ```powershell
   pip install azure-ai-ml azure-identity azure-storage-blob
   ```

2. **Login to Azure:**
   ```powershell
   az login
   ```

3. **Get subscription ID:**
   ```powershell
   az account show --query id --output tsv
   ```

4. **Update azure_config.py:**
   ```python
   SUBSCRIPTION_ID = "your-subscription-id-here"
   RESOURCE_GROUP = "your-resource-group-name"
   WORKSPACE_NAME = "your-workspace-name"
   ```

5. **Run:**
   ```powershell
   python test_azure_data.py
   ```

---

## 📊 Comparison

| Option | Time | Complexity | Best For |
|--------|------|------------|----------|
| **Local File** | 1 min | ⭐ Easy | Development & testing |
| **SAS Token** | 2 min | ⭐⭐ Medium | Quick Azure testing |
| **Azure SDK** | 10 min | ⭐⭐⭐ Advanced | Production deployment |

---

## 🚀 Quick Start (Right Now!)

Since your `data.csv` already exists, just run:

```powershell
cd C:\Users\tarik\OneDrive\Desktop\AI-Institute\projects\CPU_challenge\deploy
python test.py
```

This will:
1. Load data from local `data.csv` (53MB)
2. Filter to server 638939
3. Send to your ngrok server
4. Save predictions to `forecast_results.csv`

---

## 📁 New Files Created

| File | Purpose |
|------|---------|
| `test.py` | ✅ Fixed - uses local data.csv |
| `test_with_sas.py` | For Azure Blob with SAS token |
| `test_azure_data.py` | For Azure ML SDK with full auth |
| `AZURE_DATA_ACCESS_GUIDE.md` | Complete guide for all methods |

---

## 🔧 If Server Not Running

If you get connection error, start the server first:

```powershell
# Terminal 1: Start server
cd deploy
python server.py

# Terminal 2: Run test
cd deploy
python test.py
```

Or use your ngrok URL (already in test.py):
```python
SERVER_URL = "https://5e3ad4cf79c9.ngrok-free.app/forecast"
```

---

## ✅ What's Fixed

- ✅ test.py now uses local data.csv (not Azure URL)
- ✅ Created test_with_sas.py for Azure with SAS token
- ✅ Created test_azure_data.py for Azure with SDK
- ✅ Added complete guide in AZURE_DATA_ACCESS_GUIDE.md

---

**Try running `python test.py` now!** It should work with your local data. 🎉
