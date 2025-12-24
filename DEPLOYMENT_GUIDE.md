# ML Model Deployment - Troubleshooting Guide

## ROOT CAUSE OF THE PROBLEM ⚠️

The **main issue** was that `data.csv` in the deploy folder contained **RAW, UNPROCESSED DATA**, while the model was trained on **PREPROCESSED DATA** with:
- Encoded categorical variables (service_description, season)
- Lag features (cpu_lag_1, cpu_lag_2, cpu_lag_3)  
- Time gap calculations (time_gap_minutes)

### What Was Missing in deploy/data.csv:
1. ❌ `service_description` was text ("CPU_Usage") instead of integer (1)
2. ❌ `season` was text ("Autumn") instead of integer (3)
3. ❌ No lag features (`cpu_lag_1`, `cpu_lag_2`, `cpu_lag_3`)
4. ❌ No `time_gap_minutes` column
5. ❌ Data wasn't sorted by time
6. ❌ Contained extra columns (`parallel_flag`, `unique_services`)

**Solution:** Added all preprocessing steps from ml5.ipynb to test.py before sending data to the server.

---

## Problems Fixed

### 1. **Duplicate Imports in server.py**
   - Removed duplicate `import pandas as pd` and `from datetime import datetime`

### 2. **Missing Data Type Conversions**
   - Added automatic conversion of Timestamp column to datetime
   - Added proper integer conversion for server_id
   - Added validation for required columns

### 3. **Poor Error Handling**
   - Improved error messages with HTTP status codes
   - Added detailed logging of errors
   - Added response status checking in test.py

### 4. **Missing Dependencies**
   - Created requirements.txt with all necessary packages

## Installation Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify model file exists:**
   - Make sure `xgboost_cpu_forecaster.pkl` exists in the parent directory
   - Path: `../xgboost_cpu_forecaster.pkl`

3. **Verify data.csv format:**
   - Required columns: `server_id`, `service_description`, `Timestamp`, `cpu_lag_1`, `cpu_lag_2`, `cpu_lag_3`, `time_gap_minutes`
   - The CSV must contain historical data for the server you want to forecast

## Running the Server

1. **Start the server:**
   ```bash
   python server.py
   ```
   Server will run on http://localhost:5000

2. **In another terminal, run the test:**
   ```bash
   python test.py
   ```

## Common Issues & Solutions

### Issue 1: Model Not Found
**Error:** `FileNotFoundError: ../xgboost_cpu_forecaster.pkl`
**Solution:** Make sure you've trained and saved the model first. Run the notebook to generate the .pkl file.

### Issue 2: Server Not Found (638939)
**Error:** `No data found for this server + service`
**Solution:** Check that `data.csv` contains data for server_id 638939 with service "CPU_Usage"

### Issue 3: Missing Columns
**Error:** `Missing required columns: [...]`
**Solution:** Ensure data.csv has all required columns with correct lag features

### Issue 4: Connection Refused
**Error:** `ConnectionRefusedError`
**Solution:** Make sure server.py is running before executing test.py

## Testing with Custom Data

To test with a different server:

```python
payload = {
    "df": df_json,
    "server_id": YOUR_SERVER_ID,  # Change this
    "service_description_str": "CPU_Usage"  # Or "Windows_CPU_Usage" or "CPU_Usage_SQL"
}
```

## API Endpoint

**POST** `/forecast`

**Request Body:**
```json
{
  "df": [...],  // Array of records with historical data
  "server_id": 638939,
  "service_description_str": "CPU_Usage"
}
```

**Response (Success):**
```json
[
  {
    "Timestamp": "2024-12-24 10:00:00",
    "server_id": 638939,
    "service_description": "CPU_Usage",
    "predicted_CPU_percent": 45.2
  },
  ...
]
```

**Response (Error):**
```json
{
  "error": "Error message here",
  "server_id": 638939
}
```
