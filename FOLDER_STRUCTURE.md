# 📁 Organized Folder Structure

Your project is now organized into clean, logical folders:

```
deploy/
├── 📄 README.md                          # Main documentation
├── 📄 run_test.bat                       # Quick test batch script
│
├── 📂 api/                               # Flask REST API
│   └── server.py                         # Local prediction server
│
├── 📂 azure_ml/                          # Azure ML Pipeline Scripts
│   ├── azure_config.py                   # Azure configuration & connection
│   ├── azure_setup_checker.py            # Verification script
│   ├── register_model.py                 # Register model in Azure ML
│   ├── create_pipeline.py                # Create automated pipeline
│   ├── deploy_endpoint.py                # Deploy real-time endpoint
│   ├── prepare_data.py                   # Pipeline data preprocessing
│   └── score.py                          # Endpoint scoring script
│
├── 📂 tests/                             # Test & Client Scripts
│   ├── test.py                           # Main test client (local data)
│   ├── test_azure_data.py                # Test with Azure ML SDK
│   ├── test_with_sas.py                  # Test with Azure Blob SAS token
│   └── test_preprocessing.py             # Data preprocessing tests
│
├── 📂 data/                              # Data Files
│   ├── data.csv                          # Training/deployment data (53MB)
│   ├── eval.csv                          # Evaluation metrics
│   ├── forecast_results.csv              # Generated predictions
│   └── server_forecastability_scores.csv # Server data from Azure ML
│
├── 📂 config/                            # Configuration Files
│   ├── requirements.txt                  # Python dependencies
│   └── environments/
│       └── env_cpu_forecast.yml          # Conda environment definition
│
└── 📂 docs/                              # Documentation
    ├── START_HERE.md                     # ⭐ Start here! Entry point guide
    ├── AZURE_ML_SETUP.md                 # Detailed Azure setup guide
    ├── AZURE_ML_INTEGRATION.md           # Architecture & integration guide
    ├── AZURE_COMMANDS_REFERENCE.md       # CLI/SDK commands reference
    ├── AZURE_SOLUTION_SUMMARY.md         # Architecture overview
    ├── AZURE_QUICKSTART.py               # Interactive checklist
    ├── AZURE_DATA_ACCESS_GUIDE.md        # How to access Azure data (3 methods)
    ├── AZURE_DATA_FIX.md                 # Quick fix for data access errors
    └── DEPLOYMENT_GUIDE.md               # Deployment instructions
```

---

## 🎯 Quick Navigation

### 🚀 Getting Started
1. **First time?** → Read [docs/START_HERE.md](docs/START_HERE.md)
2. **Need help with data?** → Check [docs/AZURE_DATA_ACCESS_GUIDE.md](docs/AZURE_DATA_ACCESS_GUIDE.md)
3. **Want Azure ML?** → Follow [docs/AZURE_ML_SETUP.md](docs/AZURE_ML_SETUP.md)

### 🧪 Running Tests
```powershell
# Test with local data
cd tests
python test.py

# Test with Azure Blob (SAS token required)
python test_with_sas.py

# Test with Azure ML SDK (full auth required)
python test_azure_data.py

# Test data preprocessing
python test_preprocessing.py
```

### 🔧 Local API Development
```powershell
# Terminal 1: Start server
cd api
python server.py

# Terminal 2: Run test
cd tests
python test.py
```

### ☁️ Azure ML Deployment
```powershell
cd azure_ml

# Step 1: Verify setup
python azure_setup_checker.py

# Step 2: Register model
python register_model.py

# Step 3: Create pipeline
python create_pipeline.py

# Step 4: Deploy endpoint
python deploy_endpoint.py
```

### 📦 Configuration
```powershell
# Update Azure credentials
# Edit: azure_ml/azure_config.py

# View/update dependencies
# Edit: config/requirements.txt
# Edit: config/environments/env_cpu_forecast.yml

# Check installed packages
pip list
```

---

## 📂 Folder Purposes

### `/api/` - Flask REST API Server
- **server.py**: Local prediction server running on localhost:5000
- Use this for local development and testing
- Accepts POST requests with raw data, returns predictions

### `/azure_ml/` - Azure ML Pipeline
- **azure_config.py**: Azure connection configuration
- **register_model.py**: Upload model to Azure ML registry
- **create_pipeline.py**: Define automated ML pipeline with steps
- **deploy_endpoint.py**: Deploy model as real-time REST API
- **score.py**: Scoring script that runs on the endpoint
- **prepare_data.py**: Data preprocessing pipeline step
- **azure_setup_checker.py**: Verify Azure prerequisites

### `/tests/` - Test & Client Scripts
- **test.py**: Main test client using local data
- **test_azure_data.py**: Test using Azure ML SDK authentication
- **test_with_sas.py**: Test using Azure Blob Storage SAS token
- **test_preprocessing.py**: Test data preprocessing independently

### `/data/` - Data Files
- **data.csv**: Main training/deployment data (53MB)
- **eval.csv**: Evaluation metrics
- **forecast_results.csv**: Generated predictions output
- **server_forecastability_scores.csv**: Data from Azure ML export

### `/config/` - Configuration
- **requirements.txt**: Python package dependencies
- **environments/env_cpu_forecast.yml**: Conda environment specification

### `/docs/` - Documentation
Complete guides for all aspects of the project:
- Setup instructions
- API references
- Command references
- Architecture diagrams
- Troubleshooting guides

---

## 🔄 Common Workflows

### Workflow 1: Local Development
```
1. Start server: python api/server.py
2. In another terminal: python tests/test.py
3. Check results: data/forecast_results.csv
```

### Workflow 2: Azure ML Setup
```
1. Read: docs/START_HERE.md
2. Configure: azure_ml/azure_config.py
3. Verify: python azure_ml/azure_setup_checker.py
4. Deploy: python azure_ml/register_model.py
5. Pipeline: python azure_ml/create_pipeline.py
6. Endpoint: python azure_ml/deploy_endpoint.py
```

### Workflow 3: Access Azure Data
```
Option A: Use local data
  - File is in: data/data.csv
  - Run: python tests/test.py

Option B: Use Azure Blob SAS
  - Generate SAS token
  - Edit: tests/test_with_sas.py
  - Run: python tests/test_with_sas.py

Option C: Use Azure ML SDK
  - Setup Azure auth
  - Edit: azure_ml/azure_config.py
  - Run: python tests/test_azure_data.py
```

---

## 📋 File Relationships

```
Data Flow:
data/data.csv → tests/test.py → api/server.py → data/forecast_results.csv

Azure ML Flow:
azure_ml/azure_config.py (config)
    ↓
azure_ml/azure_setup_checker.py (verify)
    ↓
azure_ml/register_model.py (upload model)
    ↓
azure_ml/create_pipeline.py (define pipeline)
    ↓
azure_ml/deploy_endpoint.py (deploy)
    ↓
azure_ml/score.py (runs on endpoint)
```

---

## 🚨 Important Notes

### Update Imports
If you reference files in other folders, update imports:
```python
# Instead of:
# import azure_config

# Use:
import sys
sys.path.append('..')
from azure_ml.azure_config import get_ml_client

# Or run from the parent directory
# cd deploy
# python tests/test.py
```

### Run from Root
Most commands should be run from the `deploy/` folder:
```powershell
# ✅ Correct
cd deploy
python tests/test.py

# ❌ Avoid
cd deploy/tests
python test.py  # May have import issues
```

### Update Paths
If scripts reference file paths, they may need updates:
```python
# Old (when all files in same folder):
df = pd.read_csv("data.csv")

# New (with folders):
df = pd.read_csv("data/data.csv")
```

---

## 🎉 Benefits of Organization

✅ **Easier to find files** - Clear logical grouping
✅ **Better collaboration** - Team understands structure
✅ **Easier maintenance** - Separation of concerns
✅ **Scale friendly** - Add more scripts without clutter
✅ **Production-ready** - Professional structure
✅ **Clear workflows** - Documentation matches structure

---

## 📞 Need Help?

- **Setup issues?** → Check `docs/START_HERE.md`
- **Azure problems?** → Check `docs/AZURE_ML_SETUP.md`
- **Data access?** → Check `docs/AZURE_DATA_ACCESS_GUIDE.md`
- **Commands reference?** → Check `docs/AZURE_COMMANDS_REFERENCE.md`
- **Architecture questions?** → Check `docs/AZURE_ML_INTEGRATION.md`

---

**Organization complete!** 🎉 All files are now organized for easy navigation and maintenance.
