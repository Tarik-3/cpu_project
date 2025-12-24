# CPU Usage Forecasting API - Clean Architecture

## 📁 Project Structure

```
deploy/
├── server.py              # Flask API server (handles all preprocessing)
├── test.py                # Clean client (only configuration variables)
├── data.csv               # Raw historical data
├── requirements.txt       # Python dependencies
├── run_test.bat          # Windows batch script to test easily
└── DEPLOYMENT_GUIDE.md   # Detailed troubleshooting guide
```

## 🏗️ Architecture

### **Server (server.py)**
- ✅ Handles ALL data preprocessing automatically
- ✅ Encodes categorical variables (service_description, season)
- ✅ Creates lag features (cpu_lag_1, cpu_lag_2, cpu_lag_3)
- ✅ Calculates time_gap_minutes
- ✅ Sorts data chronologically
- ✅ Loads and runs the XGBoost model
- ✅ Returns 14-day forecasts (672 predictions, every 30 min)

### **Client (test.py)**
- ✅ **CLEAN & SIMPLE** - Only configuration variables
- ✅ Loads raw CSV data (no preprocessing needed)
- ✅ Sends data to server via HTTP POST
- ✅ Saves forecast results to CSV

## 🚀 Quick Start

### Option 1: Using the batch script (Windows)
```bash
run_test.bat
```

### Option 2: Manual execution

**Terminal 1 - Start Server:**
```bash
cd deploy
python server.py
```

**Terminal 2 - Run Client:**
```bash
cd deploy
python test.py
```

## ⚙️ Configuration (test.py)

All configuration is at the top of `test.py`:

```python
# ===============================================
# CONFIGURATION VARIABLES
# ===============================================
DATA_FILE = "data.csv"                  # Path to your raw data CSV
SERVER_URL = "http://localhost:5000/forecast"  # API endpoint
TARGET_SERVER_ID = 638939               # Server to forecast
TARGET_SERVICE = "CPU_Usage"            # Service type to forecast
OUTPUT_FILE = "forecast_results.csv"    # Where to save predictions
```

### Available Service Options:
- `"CPU_Usage"`
- `"Windows_CPU_Usage"`
- `"CPU_Usage_SQL"`

### To Forecast for a Different Server:
Just change `TARGET_SERVER_ID` in test.py:
```python
TARGET_SERVER_ID = 100595  # Your server ID here
```

## 📊 Input Data Requirements

Your `data.csv` should contain **raw, unprocessed data** with these columns:

| Column | Type | Description |
|--------|------|-------------|
| `server_id` | int | Server identifier |
| `Timestamp` | datetime | Observation timestamp |
| `service_id` | int | Service identifier |
| `service_description` | string | "CPU_Usage", "Windows_CPU_Usage", etc. |
| `CPU_percent` | float | CPU usage percentage |
| `hour` | int | Hour of day (0-23) |
| `day_of_week` | int | Day of week (0-6) |
| `is_weekend` | int | 1 if weekend, 0 otherwise |
| `is_working_hour` | int | 1 if working hours, 0 otherwise |
| `season` | string | "Spring", "Summer", "Autumn", "Winter" |

**Note:** The server automatically handles:
- Converting text categories to integers
- Creating lag features
- Calculating time gaps
- Sorting data chronologically

## 📤 API Endpoint

**POST** `/forecast`

**Request:**
```json
{
  "df": [...],  // Array of raw data records
  "server_id": 638939,
  "service_description_str": "CPU_Usage"
}
```

**Response (Success):**
```json
[
  {
    "Timestamp": "Wed, 24 Dec 2025 23:22:00 GMT",
    "server_id": 638939,
    "service_description": "CPU_Usage",
    "predicted_CPU_percent": 5.67
  },
  ...
]
```

**Response (Error):**
```json
{
  "error": "Error message",
  "server_id": 638939
}
```

## 🔧 Preprocessing Pipeline (Automatic on Server)

The server automatically performs these steps:

1. **Drop unnecessary columns** (parallel_flag, unique_services)
2. **Encode service_description**: "CPU_Usage" → 1, "Windows_CPU_Usage" → 2, etc.
3. **Convert Timestamp** to datetime
4. **Set proper data types** for all columns
5. **Sort data** by server_id, service_description, Timestamp
6. **Calculate time_gap_minutes** between consecutive observations
7. **Create lag features**: cpu_lag_1, cpu_lag_2, cpu_lag_3
8. **Encode season**: "Autumn" → 3, "Winter" → 0, etc.
9. **Drop NaN values** from lag calculations

## 📦 Dependencies

Install with:
```bash
pip install -r requirements.txt
```

Required packages:
- flask
- pandas
- joblib
- xgboost
- requests
- numpy
- scikit-learn

## ✅ Verification

After running `test.py`, you should see:
```
Response type: <class 'list'>
Prediction table:
                        Timestamp  predicted_CPU_percent  server_id service_description
0  Wed, 24 Dec 2025 23:22:00 GMT               5.674938     638939           CPU_Usage
1  Wed, 24 Dec 2025 23:52:00 GMT               6.018415     638939           CPU_Usage
...
Results saved to forecast_results.csv
```

## 🐛 Troubleshooting

### Server won't start
- Check if port 5000 is available
- Verify model file exists: `../xgboost_cpu_forecaster.pkl`

### "No data found for this server + service"
- Verify `data.csv` contains your TARGET_SERVER_ID
- Check that the service type exists in your data

### Connection refused
- Make sure server.py is running before test.py
- Check SERVER_URL in test.py matches the server address

For more details, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🎯 Benefits of This Architecture

✅ **Separation of Concerns**: Server handles logic, client handles configuration  
✅ **Reusability**: Can easily create multiple clients for different servers  
✅ **Maintainability**: Preprocessing logic in one place (server)  
✅ **Simplicity**: Client code is clean and easy to understand  
✅ **Flexibility**: Easy to add new services or servers via configuration  

## 📝 Example: Forecasting Multiple Servers

Create `test_multi.py`:
```python
import requests
import pandas as pd

servers = [638939, 100595, 252705]
df = pd.read_csv("data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
df_json = df.to_dict(orient="records")

for server_id in servers:
    response = requests.post(
        "http://localhost:5000/forecast",
        json={"df": df_json, "server_id": server_id, "service_description_str": "CPU_Usage"}
    )
    if response.status_code == 200:
        pd.DataFrame(response.json()).to_csv(f"forecast_{server_id}.csv", index=False)
        print(f"✓ Forecast saved for server {server_id}")
```
