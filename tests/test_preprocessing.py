"""
Simple test script to verify preprocessing works correctly
"""
import pandas as pd
from server import preprocess_data

# Load small sample
df = pd.read_csv("data.csv")
df = df[df["server_id"] == 638939].head(100)

print("Original columns:", list(df.columns))
print("Original shape:", df.shape)

# Test preprocessing
df_processed = preprocess_data(df)

print("\nProcessed columns:", list(df_processed.columns))
print("Processed shape:", df_processed.shape)

# Check for required columns
required = ["cpu_lag_1", "cpu_lag_2", "cpu_lag_3", "time_gap_minutes"]
for col in required:
    if col in df_processed.columns:
        print(f"✓ {col} exists")
    else:
        print(f"✗ {col} MISSING")

print("\nPreprocessing works correctly!" if all(c in df_processed.columns for c in required) else "\nPreprocessing FAILED!")
