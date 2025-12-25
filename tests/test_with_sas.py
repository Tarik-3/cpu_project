"""
Simple test with Azure Blob Storage using SAS token
For when you have a SAS token from Azure Storage
"""

import requests
import pandas as pd
import os

# Get the root directory of the deploy folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===============================================
# CONFIGURATION VARIABLES
# ===============================================

# OPTION 1: Azure Blob with SAS Token
# Get SAS token from Azure Portal > Storage Account > Shared access signature
# Format: https://accountname.blob.core.windows.net/container/path/file.csv?sv=2022-11-02&ss=...
AZURE_BLOB_URL_WITH_SAS = None  # Add your SAS URL here if you have one

# OPTION 2: Local file fallback
LOCAL_DATA_FILE = os.path.join(ROOT_DIR, "data", "data.csv")

# Server Configuration
SERVER_URL = "https://5e3ad4cf79c9.ngrok-free.app/forecast"
TARGET_SERVER_ID = 638939
TARGET_SERVICE = "CPU_Usage"
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "forecast_results.csv")


def load_data():
    """Load data from Azure or local file"""
    
    # Try Azure Blob with SAS token first
    if AZURE_BLOB_URL_WITH_SAS:
        try:
            print(f"📥 Loading data from Azure Blob Storage...")
            df = pd.read_csv(AZURE_BLOB_URL_WITH_SAS)
            print(f"✅ Successfully loaded {len(df)} rows from Azure")
            return df
        except Exception as e:
            print(f"❌ Failed to load from Azure: {e}")
            print("   Falling back to local file...")
    
    # Fallback to local file
    try:
        print(f"📂 Loading data from local file: {LOCAL_DATA_FILE}")
        df = pd.read_csv(LOCAL_DATA_FILE)
        print(f"✅ Successfully loaded {len(df)} rows from local file")
        return df
    except Exception as e:
        print(f"❌ Failed to load local file: {e}")
        raise


def send_forecast_request(df):
    """Send forecast request to server"""
    
    print(f"\n📊 Processing data...")
    print(f"Total rows: {len(df)}")
    
    # Filter data for target server only
    df = df[df["server_id"] == TARGET_SERVER_ID]
    print(f"Rows for server {TARGET_SERVER_ID}: {len(df)}")
    
    if len(df) == 0:
        print(f"❌ No data found for server_id {TARGET_SERVER_ID}")
        return None
    
    # Convert Timestamp to string for JSON serialization
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Keep only the raw columns needed
    raw_columns = ["server_id", "Timestamp", "service_id", "service_description", 
                   "CPU_percent", "hour", "day_of_week", "is_weekend", 
                   "is_working_hour", "season"]
    
    optional_cols = ["parallel_flag", "unique_services"]
    for col in optional_cols:
        if col in df.columns:
            raw_columns.append(col)
    
    raw_columns = [col for col in raw_columns if col in df.columns]
    df = df[raw_columns]
    df = df.fillna(0)
    
    df_json = df.to_dict(orient="records")
    print(f"📤 Sending {len(df_json)} records to server...")
    
    # Send request
    payload = {
        "data": df_json,
        "service_description": TARGET_SERVICE
    }
    
    try:
        print(f"🚀 Calling API: {SERVER_URL}")
        response = requests.post(SERVER_URL, json=payload, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            
            if "error" in result:
                print(f"❌ Server error: {result['error']}")
                return None
            
            print(f"✅ Forecast successful!")
            
            predictions_df = pd.DataFrame(result["predictions"])
            predictions_df.to_csv(OUTPUT_FILE, index=False)
            
            print(f"💾 Results saved to: {OUTPUT_FILE}")
            print(f"📊 Predictions: {len(predictions_df)}")
            print("\n📈 First 5 predictions:")
            print(predictions_df.head())
            
            return predictions_df
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("  CPU Forecast Test - Azure/Local Data")
    print("=" * 60)
    
    # Load data
    df = load_data()
    
    # Send request
    predictions = send_forecast_request(df)
    
    if predictions is not None:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
