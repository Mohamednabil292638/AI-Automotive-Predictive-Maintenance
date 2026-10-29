import os
import sys
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_telemetry_data.csv")
ANOMALY_PATH = os.path.join(BASE_DIR, "data", "vehicle_anomaly_scores.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "failure_risk_model.joblib")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "vehicle_risk_prioritization.csv")

sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from features.component_health import calculate_component_health


df = pd.read_csv(DATA_PATH)
df = df.drop_duplicates().copy()

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Component health is calculated directly from the same telemetry rows.
health_df = calculate_component_health(df)

health_columns = [
    "vehicle_id",
    "timestamp",
    "engine_health_score",
    "brake_health_score",
    "battery_health_score",
    "overall_health_score",
]

health_df = health_df[health_columns].copy()

# Preserve one health record per original telemetry row.
health_df["_row_id"] = health_df.groupby(
    ["vehicle_id", "timestamp"]
).cumcount()

anomaly_df = pd.read_csv(ANOMALY_PATH)
anomaly_df["timestamp"] = pd.to_datetime(
    anomaly_df["timestamp"],
    errors="coerce",
)

# Preserve duplicate telemetry timestamps without multiplying rows.
anomaly_df["_row_id"] = anomaly_df.groupby(
    ["vehicle_id", "timestamp"]
).cumcount()

artifact = joblib.load(MODEL_PATH)
pipeline = artifact["pipeline"]
feature_columns = artifact["feature_columns"]

X = df[feature_columns]

df["failure_probability"] = pipeline.predict_proba(X)[:, 1]

risk_df = df[
    ["vehicle_id", "timestamp", "failure_probability"]
].copy()

risk_df["_row_id"] = risk_df.groupby(
    ["vehicle_id", "timestamp"]
).cumcount()

risk_df = risk_df.merge(
    health_df,
    on=["vehicle_id", "timestamp", "_row_id"],
    how="left",
)

risk_df = risk_df.merge(
    anomaly_df[
        ["vehicle_id", "timestamp", "_row_id", "anomaly_flag", "anomaly_score"]
    ],
    on=["vehicle_id", "timestamp", "_row_id"],
    how="left",
)

risk_df["anomaly_flag"] = risk_df["anomaly_flag"].fillna(0).astype(int)
risk_df["anomaly_score"] = risk_df["anomaly_score"].fillna(0)

risk_df["anomaly_risk"] = (
    risk_df["anomaly_score"].rank(pct=True).fillna(0)
)

risk_df["health_risk"] = (
    1 - risk_df["overall_health_score"] / 100
).clip(0, 1)

risk_df["vehicle_risk_score"] = (
    0.50 * risk_df["failure_probability"]
    + 0.25 * risk_df["anomaly_risk"]
    + 0.25 * risk_df["health_risk"]
)

risk_df["vehicle_risk_score"] = (
    risk_df["vehicle_risk_score"] * 100
).round(2)

risk_df["risk_level"] = pd.cut(
    risk_df["vehicle_risk_score"],
    bins=[-np.inf, 30, 60, 80, np.inf],
    labels=["Low", "Moderate", "High", "Critical"],
)

def recommend_action(level):
    if level == "Critical":
        return "Immediate diagnostic inspection"
    if level == "High":
        return "Prioritize maintenance inspection"
    if level == "Moderate":
        return "Monitor component health"
    return "Continue routine monitoring"


risk_df["recommended_action"] = risk_df["risk_level"].apply(
    recommend_action
)

def identify_priority_component(row):
    scores = {
        "Engine": row["engine_health_score"],
        "Brake": row["brake_health_score"],
        "Battery": row["battery_health_score"],
    }
    return min(scores, key=scores.get)


risk_df["priority_component"] = risk_df.apply(
    identify_priority_component,
    axis=1,
)

risk_df = risk_df.drop(columns=["_row_id"])

risk_df.to_csv(OUTPUT_PATH, index=False)

print("=" * 60)
print("CORRECTED VEHICLE RISK PRIORITIZATION ENGINE")
print("=" * 60)
print(f"Original telemetry rows: {len(df)}")
print(f"Risk records generated: {len(risk_df)}")
print(f"Unique vehicles: {risk_df['vehicle_id'].nunique()}")
print()

print("Risk Distribution:")
print(risk_df["risk_level"].value_counts().sort_index())
print()

print("Top 10 Highest-Risk Records:")
print(
    risk_df[
        [
            "vehicle_id",
            "timestamp",
            "vehicle_risk_score",
            "risk_level",
            "priority_component",
            "recommended_action",
        ]
    ]
    .sort_values("vehicle_risk_score", ascending=False)
    .head(10)
    .to_string(index=False)
)

print()
print(f"Saved to: {OUTPUT_PATH}")
print("=" * 60)
