"""
Data Preparation Script for Azure ML Pipeline
Preprocesses raw data for model training
"""

import pandas as pd
import argparse
import os


service_description_mapping = {
    "CPU_Usage": 1,
    "Windows_CPU_Usage": 2,
    "CPU_Usage_SQL": 3
}

season_mapping = {
    "winter": 0, "spring": 1, "summer": 2, "autumn": 3,
    "Winter": 0, "Spring": 1, "Summer": 2, "Autumn": 3
}


def prepare_data(input_data, output_data):
    """Prepare and preprocess data"""
    
    print(f"Loading data from {input_data}")
    df = pd.read_csv(input_data)
    print(f"Loaded {len(df)} rows")
    
    # Drop unnecessary columns
    df = df.drop(columns=["parallel_flag", "unique_services"], errors="ignore")
    
    # Map service_description
    if df["service_description"].dtype == 'object':
        df["service_description"] = df["service_description"].map(service_description_mapping)
    
    # Convert Timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    
    # Set data types
    df = df.astype({
        "server_id": "int64",
        "service_id": "int64",
        "service_description": "int64",
        "CPU_percent": "float32",
        "hour": "int8",
        "day_of_week": "int8",
        "is_weekend": "int8",
        "is_working_hour": "int8",
    })
    
    # Sort data
    df = df.sort_values(["server_id", "service_description", "Timestamp"])
    
    # Calculate time gaps
    df["time_gap_minutes"] = (
        df.groupby(["server_id", "service_description"])["Timestamp"]
          .diff()
          .dt.total_seconds()
          .div(60)
    )
    
    # Create lag features
    df["cpu_lag_1"] = df.groupby("server_id")["CPU_percent"].shift(1)
    df["cpu_lag_2"] = df.groupby("server_id")["CPU_percent"].shift(2)
    df["cpu_lag_3"] = df.groupby("server_id")["CPU_percent"].shift(3)
    
    # Drop NaN
    df = df.dropna()
    
    # Map season
    if df["season"].dtype == 'object':
        df["season"] = df["season"].map(season_mapping)
    
    print(f"Prepared {len(df)} rows")
    
    # Save
    os.makedirs(os.path.dirname(output_data), exist_ok=True)
    df.to_csv(output_data, index=False)
    print(f"Saved to {output_data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", type=str)
    parser.add_argument("--output_data", type=str)
    args = parser.parse_args()
    
    prepare_data(args.input_data, args.output_data)
