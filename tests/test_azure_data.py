"""
Test script for Azure ML data with proper authentication
Downloads data from Azure ML datastore and sends to local/deployed server
"""

import requests
import pandas as pd
import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import sys

# Get the root directory of the deploy folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from azure_ml.azure_config import get_ml_client, SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME

# ===============================================
# CONFIGURATION VARIABLES
# ===============================================
# Azure ML Data Configuration
AZURE_DATA_PATH = "UI/2025-12-24_111626_UTC/server_forecastability_scores.csv"  # Path in Azure ML datastore
DATASTORE_NAME = "workspaceblobstore"  # Default datastore name

# Server Configuration
SERVER_URL = "https://5e3ad4cf79c9.ngrok-free.app/forecast"  # Update with your ngrok or Azure endpoint
TARGET_SERVER_ID = 638939
TARGET_SERVICE = "CPU_Usage"  # Options: "CPU_Usage", "Windows_CPU_Usage", "CPU_Usage_SQL"
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "forecast_results.csv")

# Fallback: Use local file if Azure fails
LOCAL_DATA_FILE = os.path.join(ROOT_DIR, "data", "data.csv")
USE_LOCAL_FALLBACK = True


def download_data_from_azure():
    """
    Download data from Azure ML datastore using authentication
    """
    try:
        print("🔐 Authenticating with Azure ML...")
        ml_client = get_ml_client()
        
        print(f"📦 Connected to workspace: {WORKSPACE_NAME}")
        
        # Get the datastore
        print(f"🔍 Accessing datastore: {DATASTORE_NAME}")
        datastore = ml_client.datastores.get(DATASTORE_NAME)
        
        # Build the full URI
        # Format: azureml://subscriptions/{sub}/resourcegroups/{rg}/workspaces/{ws}/datastores/{ds}/paths/{path}
        data_uri = (
            f"azureml://subscriptions/{SUBSCRIPTION_ID}/"
            f"resourcegroups/{RESOURCE_GROUP}/"
            f"workspaces/{WORKSPACE_NAME}/"
            f"datastores/{DATASTORE_NAME}/"
            f"paths/{AZURE_DATA_PATH}"
        )
        
        print(f"📥 Downloading data from Azure ML...")
        print(f"   URI: {data_uri}")
        
        # Download using Azure ML SDK
        from azure.ai.ml.constants import AssetTypes
        from azure.ai.ml.entities import Data
        
        # Read data directly using mltable or download
        # For CSV files, we can use pandas with azure credentials
        from azure.storage.blob import BlobServiceClient
        
        # Get storage account credentials
        credential = DefaultAzureCredential()
        
        # Extract blob storage info from datastore
        account_url = datastore.account_name
        container_name = datastore.container_name
        
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_url}.blob.core.windows.net",
            credential=credential
        )
        
        # Get blob client
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=AZURE_DATA_PATH
        )
        
        # Download to memory
        print("   Downloading blob...")
        blob_data = blob_client.download_blob()
        
        # Read into pandas
        import io
        df = pd.read_csv(io.BytesIO(blob_data.readall()))
        
        print(f"✅ Successfully downloaded data: {len(df)} rows")
        return df
        
    except Exception as e:
        print(f"❌ Failed to download from Azure ML: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        if USE_LOCAL_FALLBACK:
            print(f"\n📂 Falling back to local file: {LOCAL_DATA_FILE}")
            try:
                df = pd.read_csv(LOCAL_DATA_FILE)
                print(f"✅ Loaded local data: {len(df)} rows")
                return df
            except Exception as local_error:
                print(f"❌ Local fallback also failed: {local_error}")
                raise
        else:
            raise


def send_forecast_request(df):
    """
    Send forecast request to server (same as original test.py)
    """
    print(f"\n📊 Processing data...")
    print(f"Total rows: {len(df)}")
    
    # Filter data for target server only (to reduce data size)
    df = df[df["server_id"] == TARGET_SERVER_ID]
    print(f"Rows for server {TARGET_SERVER_ID}: {len(df)}")
    
    if len(df) == 0:
        print(f"❌ No data found for server_id {TARGET_SERVER_ID}")
        return None
    
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
    
    # Filter to existing columns only
    raw_columns = [col for col in raw_columns if col in df.columns]
    df = df[raw_columns]
    
    # Fill NaN values to make JSON serialization possible
    df = df.fillna(0)
    
    # Convert to JSON records
    df_json = df.to_dict(orient="records")
    print(f"📤 Sending {len(df_json)} records to server...")
    
    # ===============================================
    # SEND REQUEST TO SERVER
    # ===============================================
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
            
            # Convert predictions to DataFrame
            predictions_df = pd.DataFrame(result["predictions"])
            
            # Save to CSV
            predictions_df.to_csv(OUTPUT_FILE, index=False)
            print(f"💾 Results saved to: {OUTPUT_FILE}")
            print(f"📊 Predictions generated: {len(predictions_df)}")
            
            # Display first few predictions
            print("\n📈 First 5 predictions:")
            print(predictions_df.head())
            
            return predictions_df
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def main():
    """Main execution flow"""
    print("=" * 60)
    print("  Azure ML Data Test Script")
    print("=" * 60)
    
    # Step 1: Download data from Azure ML
    print("\n[STEP 1] Downloading data from Azure ML")
    df = download_data_from_azure()
    
    if df is None:
        print("❌ Failed to load data. Exiting.")
        return
    
    # Step 2: Send forecast request
    print("\n[STEP 2] Sending forecast request to server")
    predictions = send_forecast_request(df)
    
    if predictions is not None:
        print("\n✅ Test completed successfully!")
        print(f"📄 Output file: {OUTPUT_FILE}")
    else:
        print("\n❌ Test failed!")


if __name__ == "__main__":
    main()
