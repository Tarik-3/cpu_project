import requests
import pandas as pd
import os

# Get the root directory of the deploy folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===============================================
# CONFIGURATION VARIABLES
# ===============================================
DATA_FILE = os.path.join(ROOT_DIR, "data", "data.csv")  # Local data file to send
SERVER_URL = "https://5e3ad4cf79c9.ngrok-free.app/forecast"
TARGET_SERVER_ID = 638939
TARGET_SERVICE = "CPU_Usage"  # Options: "CPU_Usage", "Windows_CPU_Usage", "CPU_Usage_SQL"
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "forecast_results.csv")

# ===============================================
# LOAD RAW DATA
# ===============================================
print(f"Loading data from {DATA_FILE}...")
df = pd.read_csv(DATA_FILE)
print(f"Total rows: {len(df)}")

# Filter data for target server only (to reduce data size)
df = df[df["server_id"] == TARGET_SERVER_ID]
print(f"Rows for server {TARGET_SERVER_ID}: {len(df)}")

# Convert Timestamp to string for JSON serialization
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

# Keep only the raw columns needed (server will create lag features)
raw_columns = ["server_id", "Timestamp", "service_id", "service_description", 
               "CPU_percent", "hour", "day_of_week", "is_weekend", 
               "is_working_hour", "season"]

# Include optional columns if they exist
optional_cols = ["parallel_flag", "unique_services"]
for col in optional_cols:
    if col in df.columns:
        raw_columns.append(col)

df = df[raw_columns]

# Fill NaN values to make JSON serialization possible
df = df.fillna(0)

# Convert to JSON records
df_json = df.to_dict(orient="records")
print(f"Sending {len(df_json)} records to server...")

# ===============================================
# SEND REQUEST TO SERVER
# ===============================================
payload = {
    "df": df_json,
    "server_id": TARGET_SERVER_ID,
    "service_description_str": TARGET_SERVICE
}

response = requests.post(SERVER_URL, json=payload)

# Check response status
if response.status_code != 200:
    print(f"Error: Server returned status code {response.status_code}")
    print(f"Response: {response.text}")
else:
    # Convert JSON response to DataFrame
    result_json = response.json()
    print(f"Response type: {type(result_json)}")
    
    # If the server returned an error, handle it
    if isinstance(result_json, dict) and "error" in result_json:
        print("Error:", result_json)
    else:
        result_df = pd.DataFrame(result_json)
        print("Prediction table:\n", result_df.head())

        # Save to CSV
        result_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Results saved to {OUTPUT_FILE}")