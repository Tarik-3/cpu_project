from flask import Flask, request, jsonify
import joblib
import pandas as pd
from datetime import datetime

service_description_mapping = {
    "CPU_Usage": 1,
    "Windows_CPU_Usage": 2,
    "CPU_Usage_SQL": 3
}

season_mapping = {
    "winter": 0,
    "spring": 1,
    "summer": 2,
    "autumn": 3,
    "Winter": 0,
    "Spring": 1,
    "Summer": 2,
    "Autumn": 3
}


def preprocess_data(df):
    """
    Preprocess raw data: encode categories, create lag features, calculate time gaps.
    This matches the preprocessing done in ml5.ipynb.
    """
    # 1. Drop unnecessary columns
    df = df.drop(columns=["parallel_flag", "unique_services"], errors="ignore")
    
    # 2. Map service_description to integers (if it's text)
    if df["service_description"].dtype == 'object':
        df["service_description"] = df["service_description"].map(service_description_mapping)
    
    # 3. Convert Timestamp and set data types
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    
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
    
    # 4. Sort data (CRITICAL for time series)
    df = df.sort_values(["server_id", "service_description", "Timestamp"])
    
    # 5. Calculate time_gap_minutes
    df["time_gap_minutes"] = (
        df.groupby(["server_id", "service_description"])["Timestamp"]
          .diff()
          .dt.total_seconds()
          .div(60)
    )
    
    # 6. Create lag features
    df["cpu_lag_1"] = df.groupby("server_id")["CPU_percent"].shift(1)
    df["cpu_lag_2"] = df.groupby("server_id")["CPU_percent"].shift(2)
    df["cpu_lag_3"] = df.groupby("server_id")["CPU_percent"].shift(3)
    
    # 7. Drop rows with NaN values
    df = df.dropna()
    
    # 8. Map season to integers (if it's text)
    if df["season"].dtype == 'object':
        df["season"] = df["season"].map(season_mapping)
    
    return df


def get_season_from_date(ts):
    month = ts.month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"


def forecast_14_days(
    model,
    df,
    server_id,
    service_description_str,
    steps=14 * 48
):
    # -------------------------------------------------
    # 1. SORT DATA (CRITICAL)
    # -------------------------------------------------
    df = df.sort_values(
        ["server_id", "service_description", "Timestamp"]
    )

    # -------------------------------------------------
    # 2. FILTER SERVER + SERVICE
    # -------------------------------------------------
    df_srv = df[
        (df["server_id"] == server_id) &
        (df["service_description"] == service_description_mapping[service_description_str])
    ]

    if df_srv.empty:
        raise ValueError("No data found for this server + service")

    # -------------------------------------------------
    # 3. TAKE LAST ROW (LAGS + GAP SOURCE)
    # -------------------------------------------------
    last = df_srv.iloc[-1].copy()

    # -------------------------------------------------
    # 4. FORCE DATA TYPES (IMPORTANT)
    # -------------------------------------------------
    last["cpu_lag_1"] = float(last["cpu_lag_1"])
    last["cpu_lag_2"] = float(last["cpu_lag_2"])
    last["cpu_lag_3"] = float(last["cpu_lag_3"])
    last["time_gap_minutes"] = float(last["time_gap_minutes"])

    # -------------------------------------------------
    # 5. START FROM CURRENT COMPUTER TIME
    # -------------------------------------------------
    current_ts = pd.Timestamp.now().floor("min")

    future_rows = []

    for _ in range(steps):

        # -------- calendar features --------
        hour = int(current_ts.hour)
        day_of_week = int(current_ts.dayofweek)
        is_weekend = int(day_of_week >= 5)
        is_working_hour = int(8 <= hour <= 18 and not is_weekend)

        season_str = get_season_from_date(current_ts)
        season = int(season_mapping[season_str])

        # -------- model input --------
        X_next = pd.DataFrame([{
            "cpu_lag_1": last["cpu_lag_1"],
            "cpu_lag_2": last["cpu_lag_2"],
            "cpu_lag_3": last["cpu_lag_3"],
            "time_gap_minutes": 30.0,  # FORCED
            "hour": hour,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "is_working_hour": is_working_hour,
            "season": season,
            "service_description": service_description_mapping[service_description_str],
        }])

        # -------- prediction --------
        pred_cpu = float(model.predict(X_next)[0])

        future_rows.append({
            "Timestamp": current_ts,
            "server_id": server_id,
            "service_description": service_description_str,
            "predicted_CPU_percent": pred_cpu
        })

        # -------- update lags --------
        last["cpu_lag_3"] = last["cpu_lag_2"]
        last["cpu_lag_2"] = last["cpu_lag_1"]
        last["cpu_lag_1"] = pred_cpu

        # -------- advance time --------
        current_ts += pd.Timedelta(minutes=30)

    return pd.DataFrame(future_rows)

# Your mappings and helper functions here (service_description_mapping, season_mapping, get_season_from_date, forecast_14_days)






# Load model
model = joblib.load("../xgboost_cpu_forecaster.pkl")



app = Flask(__name__)

@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        data = request.get_json()
        print(f"Received request for server_id: {data.get('server_id')}")
        
        df = pd.DataFrame(data["df"])
        print(f"DataFrame shape before preprocessing: {df.shape}")
        print(f"Columns before preprocessing: {list(df.columns)}")
        
        # Preprocess the raw data
        df = preprocess_data(df)
        print(f"DataFrame shape after preprocessing: {df.shape}")
        print(f"Columns after preprocessing: {list(df.columns)}")
        
        server_id = int(data["server_id"])
        service_description_str = data["service_description_str"]

        result = forecast_14_days(
            model=model,
            df=df,
            server_id=server_id,
            service_description_str=service_description_str
        )

        print(f"Forecast generated: {len(result)} predictions")
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "server_id": data.get("server_id", "unknown")}), 500

    
if __name__ == "__main__":
    app.run(port=5000)
