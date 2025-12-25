# 🖥️ Using Azure ML Compute Instance

## What is a Compute Instance?

A **compute instance** is a managed cloud-based workstation in Azure ML that provides:
- ✅ Pre-configured Python environment
- ✅ Jupyter notebooks
- ✅ VS Code in browser
- ✅ Terminal access
- ✅ GPU/CPU options
- ✅ No local setup needed

**Perfect for your project!** You'll run everything in the cloud.

---

## 🎯 Your Workflow with Compute Instance

### Before (Local)
```
Your PC → Python → Model → Test
```

### Now (Cloud)
```
Azure ML Compute Instance → Python → Model → Deploy Endpoint
```

**Benefits:**
- No local dependencies needed
- More powerful compute
- Direct access to Azure ML resources
- Persistent storage
- Auto-shutdown to save costs

---

## 📋 Step-by-Step Setup

### Step 1: Create Compute Instance (Azure Portal)

1. **Go to Azure ML Studio:**
   - https://ml.azure.com
   - Sign in with your account
   - Select workspace: `cpu-project`
   - Resource group: `RG_JIT02`

2. **Create Compute Instance:**
   - Left menu → **Compute**
   - Tab: **Compute instances**
   - Click: **+ New**
   
3. **Configure:**
   ```
   Compute name: cpu-forecast-instance
   Virtual machine type: CPU
   Virtual machine size: Standard_DS3_v2
   ```
   
4. **Click:** Create (takes 3-5 minutes)

### Step 2: Upload Your Project Files

**Option A: Using Azure ML Studio UI**
1. Left menu → **Notebooks**
2. Click **Upload files** 
3. Upload from `deploy/` folder:
   - All files in `azure_ml/`
   - All files in `tests/`
   - All files in `data/` (or just use Azure ML datasets)
   - `config/requirements.txt`

**Option B: Using Terminal (after compute starts)**
```bash
# On your compute instance terminal
git clone <your-repo-url>
# Or upload via file browser
```

### Step 3: Install Dependencies

**On compute instance terminal:**
```bash
cd <your-project-folder>
pip install -r config/requirements.txt
```

### Step 4: Run Your Scripts

```bash
# Register model
python azure_ml/register_model.py

# Create pipeline
python azure_ml/create_pipeline.py

# Deploy endpoint
python azure_ml/deploy_endpoint.py
```

---

## 🔧 What Changes for Compute Instance

### Files to Upload
```
Upload to compute instance:
├── azure_ml/
│   ├── azure_config.py
│   ├── register_model.py
│   ├── create_pipeline.py
│   ├── deploy_endpoint.py
│   ├── score.py
│   └── prepare_data.py
├── data/
│   └── data.csv (or use Azure ML datasets)
├── config/
│   └── requirements.txt
└── xgboost_cpu_forecaster.pkl (your trained model)
```

### Authentication
✅ **Automatic!** Compute instances have built-in authentication
- No need for `az login`
- DefaultAzureCredential works automatically
- Already connected to your workspace

### Paths
Update file paths to use compute instance paths:
```python
# Instead of local paths
DATA_FILE = "/home/azureuser/cloudfiles/code/data/data.csv"
MODEL_FILE = "/home/azureuser/cloudfiles/code/xgboost_cpu_forecaster.pkl"
```

---

## 💰 Cost Management

### Auto-shutdown
```
Settings → Schedule
- Auto-shutdown: Enabled
- Time: 7:00 PM (or your preference)
- Time zone: Your timezone
```

### Manual Stop
When not using:
```
Azure ML Studio → Compute → Your instance → Stop
```

**Cost:** ~$0.20-0.50/hour (Standard_DS3_v2)

---

## 🚀 Quick Start Commands (On Compute Instance)

### 1. Open Terminal
```
Azure ML Studio → Compute → Your instance → Terminal
```

### 2. Install Dependencies
```bash
pip install flask pandas joblib xgboost requests numpy scikit-learn
pip install azure-ai-ml azure-identity azure-storage-blob
```

### 3. Verify Azure Connection
```bash
python azure_ml/azure_config.py
# Should show: ✅ Connected to workspace: cpu-project
```

### 4. Upload Model File
Upload `xgboost_cpu_forecaster.pkl` via file browser

### 5. Register Model
```bash
python azure_ml/register_model.py
```

### 6. Deploy Endpoint
```bash
python azure_ml/deploy_endpoint.py
```

---

## 📊 Compute Instance vs Local

| Feature | Local PC | Compute Instance |
|---------|----------|------------------|
| **Setup** | Install Python, packages | Pre-configured |
| **Authentication** | Need `az login` | Automatic |
| **Power** | Limited by PC | Scalable (GPU/CPU) |
| **Cost** | Free (your PC) | ~$0.20-0.50/hour |
| **Access to Azure** | Via SDK | Direct connection |
| **Persistence** | Your PC storage | Cloud storage |
| **Collaboration** | Hard to share | Easy sharing |

---

## 🎓 Using Jupyter Notebooks on Compute Instance

### Upload Your Notebook
1. Azure ML Studio → Notebooks
2. Upload `ml5.ipynb`
3. Select compute instance
4. Run cells

### Or Create New Notebook
```python
# Cell 1: Install packages
!pip install xgboost pandas scikit-learn

# Cell 2: Import and train
import pandas as pd
import xgboost as xgb
# ... your training code

# Cell 3: Register model
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
# ... registration code
```

---

## 🔄 Your New Workflow

### Development
```
1. Start compute instance (Azure Portal)
2. Open terminal or notebook
3. Edit/run code in cloud
4. Test directly in Azure ML
5. Stop instance when done
```

### Deployment
```
1. Register model (on compute instance)
2. Create pipeline (on compute instance)
3. Deploy endpoint (on compute instance)
4. Test endpoint (from anywhere)
```

### Testing
```
# Can still test from your local PC
python tests/test.py  # Points to Azure endpoint
```

---

## 📁 Recommended File Structure on Compute Instance

```
/home/azureuser/cloudfiles/code/Users/<your-name>/
└── cpu-project/
    ├── azure_ml/
    ├── data/
    ├── config/
    ├── models/
    │   └── xgboost_cpu_forecaster.pkl
    └── notebooks/
        └── ml5.ipynb
```

---

## ✅ Advantages for Your Project

1. **No Local Setup**
   - Pre-installed Python
   - Pre-configured Azure SDK
   - No environment issues

2. **Built-in Authentication**
   - Automatic workspace connection
   - No `az login` needed
   - Seamless Azure integration

3. **Better Performance**
   - More CPU/RAM than typical PC
   - Optional GPU for training
   - Faster data access

4. **Collaboration Ready**
   - Share notebooks
   - Team access
   - Version control integration

5. **Production-like Environment**
   - Same environment as deployment
   - Test in cloud conditions
   - Easier debugging

---

## 🎯 Next Steps for You

### Immediate (10 minutes)
1. **Create compute instance** in Azure ML Studio
2. **Wait for provisioning** (3-5 minutes)
3. **Open terminal** on instance
4. **Upload files** via file browser

### Setup (10 minutes)
1. **Install packages:** `pip install -r config/requirements.txt`
2. **Upload model file:** `xgboost_cpu_forecaster.pkl`
3. **Test connection:** `python azure_ml/azure_config.py`

### Deploy (20 minutes)
1. **Register model:** `python azure_ml/register_model.py`
2. **Deploy endpoint:** `python azure_ml/deploy_endpoint.py`
3. **Test endpoint:** From anywhere!

---

## 💡 Pro Tips

### 1. Use Persistent Storage
Your files in `/home/azureuser/cloudfiles/` persist even if instance stops.

### 2. Schedule Auto-shutdown
Save costs by auto-stopping at night.

### 3. Use Git
```bash
git clone <your-repo>
git pull  # Get latest changes
```

### 4. Monitor Costs
Azure Portal → Cost Management → Check daily costs

### 5. Use Notebooks
Great for interactive development and documentation.

---

## 🆘 Troubleshooting

### "Compute instance not starting"
- Check quota limits in Azure Portal
- Try smaller VM size

### "Can't upload files"
- Use compute instance file browser
- Or use terminal: `wget` or `git clone`

### "Package not found"
```bash
pip install <package-name>
# Or
pip install -r config/requirements.txt
```

### "Authentication failed"
- Should not happen! Compute instances auto-authenticate
- Check workspace connection in azure_config.py

---

## 📞 Quick Reference

| Task | Command/Location |
|------|-----------------|
| Create instance | Azure ML Studio → Compute → New |
| Start instance | Compute → Your instance → Start |
| Stop instance | Compute → Your instance → Stop |
| Open terminal | Compute → Your instance → Terminal |
| Open Jupyter | Compute → Your instance → Jupyter |
| Upload files | Notebooks → Upload |
| Install packages | Terminal: `pip install ...` |
| Run script | Terminal: `python script.py` |

---

## ✨ Summary

**You chose:** Compute instance ✅
**Benefit:** No local setup, direct Azure access, auto-authenticated
**Cost:** ~$0.20-0.50/hour (stop when not using)
**Next:** Create instance in Azure ML Studio

**This is the recommended approach for Azure ML projects!** 🚀

---

**Ready to start?**
1. Go to https://ml.azure.com
2. Create compute instance
3. Upload your files
4. Run your scripts!
