# 🎯 How to Run Tests

After organizing the files into folders, here's how to run each test.

## ⚡ Quick Start

```powershell
# Run from the deploy folder
cd C:\Users\tarik\OneDrive\Desktop\AI-Institute\projects\CPU_challenge\deploy

# Run the main test
python tests/test.py

# Check results
type data\forecast_results.csv | head -5
```

---

## 🧪 All Test Options

### 1. Test with Local Data ⭐ RECOMMENDED
```powershell
cd deploy
python tests/test.py
```

**What it does:**
- Loads: `data/data.csv` (53MB)
- Filters to: server 638939
- Sends to: ngrok server
- Saves to: `data/forecast_results.csv`

**Status:** ✅ Working

---

### 2. Test with Azure ML SDK
```powershell
cd deploy
python tests/test_azure_data.py
```

**Prerequisites:**
1. Install packages:
   ```powershell
   pip install azure-ai-ml azure-identity azure-storage-blob
   ```

2. Login to Azure:
   ```powershell
   az login
   ```

3. Update `azure_ml/azure_config.py`:
   ```python
   SUBSCRIPTION_ID = "your-subscription-id"
   RESOURCE_GROUP = "your-resource-group"
   WORKSPACE_NAME = "your-workspace-name"
   ```

**What it does:**
- Downloads data from Azure ML datastore
- Uses proper authentication
- Falls back to local data if Azure fails
- Sends to server

---

### 3. Test with Azure Blob SAS Token
```powershell
cd deploy
python tests/test_with_sas.py
```

**Prerequisites:**
1. Generate SAS token from Azure Portal:
   - Storage Accounts → `cpuproject9177426007`
   - Shared access signature
   - Set Read + List permissions
   - Generate SAS URL

2. Add to `tests/test_with_sas.py`:
   ```python
   AZURE_BLOB_URL_WITH_SAS = "https://cpuproject9177426007.blob.core.windows.net/...?sv=..."
   ```

**What it does:**
- Downloads from Azure Blob with SAS token
- Falls back to local data if fails
- Sends to server

---

### 4. Test Data Preprocessing
```powershell
cd deploy
python tests/test_preprocessing.py
```

**What it does:**
- Tests preprocessing pipeline independently
- Validates data transformations
- Shows encoding, lags, feature engineering

---

## 🚀 Test with Local Server

Run server and test together:

**Terminal 1: Start Server**
```powershell
cd deploy
python api/server.py
```

**Terminal 2: Run Test**
```powershell
cd deploy
python tests/test.py
```

**Expected Output:**
```
Loading data from ...data/data.csv...
Total rows: 668087
Rows for server 638939: 4973
Sending 4973 records to server...
Results saved to ...data/forecast_results.csv
```

---

## 📊 Test Results

After running tests, check results:

```powershell
# View first few predictions
type data\forecast_results.csv | head -10

# Count predictions
(Get-Content data\forecast_results.csv | Measure-Object -Line).Lines - 1
# Should be 672 predictions

# View in Excel (if available)
invoke-item data\forecast_results.csv
```

---

## 🐛 Troubleshooting Tests

### "No such file or directory: data.csv"
**Solution:** Ensure you run from `deploy` folder:
```powershell
cd deploy  # Important!
python tests/test.py
```

### "Connection refused" (server error)
**Solution:** Start the server first:
```powershell
# Terminal 1
python api/server.py

# Terminal 2 (in another terminal)
python tests/test.py
```

### "Azure authentication failed"
**Solution:** Make sure you logged in:
```powershell
az login
az account show
```

### "File not found: forecast_results.csv"
**Solution:** Results save to `data/` folder after running test. Check:
```powershell
dir data\forecast_results.csv
```

---

## 📁 File Structure Used by Tests

```
deploy/
├── api/
│   └── server.py              ← Runs on localhost:5000
├── tests/
│   ├── test.py                ← Main test (uses data/data.csv)
│   ├── test_azure_data.py     ← Uses Azure ML SDK
│   ├── test_with_sas.py       ← Uses Azure Blob SAS
│   └── test_preprocessing.py  ← Tests preprocessing
├── data/
│   ├── data.csv               ← Input data (used by tests)
│   ├── forecast_results.csv   ← Output (created by tests)
│   └── eval.csv               ← Evaluation metrics
└── azure_ml/
    └── azure_config.py        ← Configuration (used by azure tests)
```

---

## 🔧 Key Points

1. **Always run from `deploy/` folder:**
   ```powershell
   cd deploy
   python tests/test.py  # ✅ Correct
   ```

2. **Paths are automatic:**
   - Tests use `os.path` to find data automatically
   - No need to manually set paths

3. **Default test uses local data:**
   - `test.py` works immediately
   - No Azure login or configuration needed

4. **Results saved automatically:**
   - `data/forecast_results.csv` created after run
   - Contains 672 predictions for 14 days

---

## ✅ Success Indicators

After running `python tests/test.py`, you should see:
```
✅ Loading data from .../data/data.csv...
✅ Total rows: 668087
✅ Rows for server 638939: 4973
✅ Sending 4973 records to server...
✅ Results saved to .../data/forecast_results.csv
```

---

## 📞 More Help

- Documentation: `docs/START_HERE.md`
- Data access: `docs/AZURE_DATA_ACCESS_GUIDE.md`
- Azure setup: `docs/AZURE_ML_SETUP.md`
- Commands: `docs/AZURE_COMMANDS_REFERENCE.md`

---

**Ready to test?** Run: `cd deploy && python tests/test.py`
