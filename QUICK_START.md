# 🎯 Quick Start - After Organization

Your files are now organized! Here's how to get started right away.

## ⚡ 30-Second Quick Start

```powershell
cd C:\Users\tarik\OneDrive\Desktop\AI-Institute\projects\CPU_challenge\deploy

# Run the test
python tests/test.py

# Check results
type data\forecast_results.csv | head -5
```

✅ Done! You just ran the model and got predictions.

---

## 📚 By Use Case

### 🧪 "I want to test the model"
```powershell
cd deploy
python tests/test.py
# Results saved to: data/forecast_results.csv
```

### 🚀 "I want to start the API server"
```powershell
cd deploy
python api/server.py
# Server runs on: http://localhost:5000
```

### ☁️ "I want to deploy to Azure"
```powershell
cd deploy\azure_ml
python azure_setup_checker.py
python register_model.py
python create_pipeline.py
python deploy_endpoint.py
```

### 📖 "I want to understand the project"
```powershell
cd deploy\docs
# Open START_HERE.md with your editor
```

---

## 🗂️ Folder Guide

| Folder | Purpose | Run |
|--------|---------|-----|
| `api/` | Flask REST API | `python api/server.py` |
| `azure_ml/` | Azure ML scripts | `python azure_ml/azure_setup_checker.py` |
| `tests/` | Test scripts | `python tests/test.py` |
| `data/` | Data files | View: `type data/data.csv` |
| `config/` | Configuration | View: `type config/requirements.txt` |
| `docs/` | Documentation | Read: `docs/START_HERE.md` |

---

## 🚦 Step-by-Step for First Time

### Step 1: Verify Everything Works (2 minutes)
```powershell
cd deploy
python tests/test.py
```

Expected output:
```
Loading data from .../data/data.csv...
Total rows: 668087
Rows for server 638939: 4973
Sending 4973 records to server...
Results saved to .../data/forecast_results.csv
```

### Step 2: Check Results (1 minute)
```powershell
# View predictions
type data\forecast_results.csv | head -10

# Count how many predictions (should be 672)
(Get-Content data\forecast_results.csv | Measure-Object -Line).Lines
```

### Step 3: Understand the Project (10 minutes)
```powershell
# Read the main guide
notepad docs\START_HERE.md

# Read folder organization
notepad FOLDER_STRUCTURE.md

# Read how to run tests
notepad HOW_TO_RUN_TESTS.md
```

### Step 4: Try Different Tests (optional)
```powershell
# Test with Azure ML SDK
python tests/test_azure_data.py

# Test with SAS token
python tests/test_with_sas.py

# Test preprocessing
python tests/test_preprocessing.py
```

### Step 5: Deploy to Azure (30 minutes)
```powershell
cd azure_ml

# 1. Update azure_config.py with your Azure subscription ID
notepad azure_config.py

# 2. Verify setup
python azure_setup_checker.py

# 3. Register model
python register_model.py

# 4. Create pipeline
python create_pipeline.py

# 5. Deploy endpoint
python deploy_endpoint.py
```

---

## 🔗 Key Files

### Most Important
- ⭐ `docs/START_HERE.md` - Read this first
- ⭐ `tests/test.py` - Run this to test
- ⭐ `FOLDER_STRUCTURE.md` - Understand organization

### Configuration
- `azure_ml/azure_config.py` - Edit for Azure setup
- `config/requirements.txt` - Python packages

### Running Code
- `api/server.py` - Start the server
- `tests/test.py` - Main test
- `azure_ml/azure_setup_checker.py` - Verify Azure

### Documentation
- `docs/AZURE_ML_SETUP.md` - Azure setup guide
- `docs/AZURE_DATA_ACCESS_GUIDE.md` - How to get data
- `docs/AZURE_COMMANDS_REFERENCE.md` - Azure commands

---

## ✅ Verification Checklist

After organization, verify everything:

```powershell
cd deploy

# ✅ Check folders exist
dir api
dir azure_ml
dir tests
dir data
dir config
dir docs

# ✅ Check test works
python tests/test.py

# ✅ Check results exist
type data\forecast_results.csv

# ✅ Check git
git log --oneline -5

# ✅ Check server starts (press Ctrl+C after starting)
python api/server.py

# ✅ Check Azure setup checker
python azure_ml/azure_setup_checker.py
```

All green? You're good to go! ✨

---

## 🎯 Next Steps

1. ✅ **Organization done** - You have clean folder structure
2. 🧪 **Verify tests work** - Run `python tests/test.py`
3. 📖 **Read documentation** - Start with `docs/START_HERE.md`
4. ☁️ **Setup Azure** - Follow `docs/AZURE_ML_SETUP.md`
5. 🚀 **Deploy model** - Run `azure_ml/deploy_endpoint.py`

---

## 💡 Pro Tips

### Tip 1: Always run from `deploy/` folder
```powershell
# ✅ Correct
cd deploy
python tests/test.py

# ❌ Wrong
cd deploy\tests
python test.py
```

### Tip 2: Use absolute paths in configurations
Files already use `os.path` for automatic path discovery.

### Tip 3: Keep `azure_config.py` secure
Never commit Azure credentials. File is in `.gitignore`.

### Tip 4: Test after changes
Run `python tests/test.py` after any code changes.

### Tip 5: Check git status
```powershell
git status
git log --oneline -5
git diff
```

---

## 🚨 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "File not found" | Run from `deploy/` folder |
| "Connection refused" | Start server: `python api/server.py` |
| "Azure auth failed" | Run: `az login` and `az account show` |
| "No module named" | Install: `pip install -r config/requirements.txt` |
| "Path not found" | Use absolute paths with `os.path` |

---

## 📞 Help Resources

| Need | Location |
|------|----------|
| **Get started** | `docs/START_HERE.md` |
| **Understand structure** | `FOLDER_STRUCTURE.md` |
| **Run tests** | `HOW_TO_RUN_TESTS.md` |
| **Setup Azure** | `docs/AZURE_ML_SETUP.md` |
| **Access data** | `docs/AZURE_DATA_ACCESS_GUIDE.md` |
| **Commands** | `docs/AZURE_COMMANDS_REFERENCE.md` |
| **Architecture** | `docs/AZURE_ML_INTEGRATION.md` |

---

## 🎉 You're All Set!

Your project is now:
- ✅ Organized into logical folders
- ✅ Documented with 10+ guides
- ✅ Ready to run tests
- ✅ Ready to deploy to Azure
- ✅ Version controlled with git

**Next step:** Run `python tests/test.py` to verify everything works!

---

Questions? Check the documentation in `docs/` folder.

Happy coding! 🚀
