import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_telemetry_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_detector.joblib")

os.makedirs(MODEL_DIR, exist_ok=True)


ANOMALY_FEATURES = [
    "engine_temp_c",
    "engine_rpm",
    "oil_pressure_psi",
    "coolant_temp_c",
    "engine_load_percent",
    "exhaust_gas_temp_c",
    "vibration_level",
    "brake_fluid_level_psi",
    "brake_pad_wear_mm",
    "brake_temp_c",
    "battery_voltage_v",
    "battery_current_a",
    "battery_temp_c",
    "alternator_output_v",
    "battery_charge_percent",
    "battery_health_percent",
]


df = pd.read_csv(DATA_PATH)
df = df.drop_duplicates().copy()

features = [c for c in ANOMALY_FEATURES if c in df.columns]
X = df[features].apply(pd.to_numeric, errors="coerce")


pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        (
            "model",
            IsolationForest(
                n_estimators=200,
                contamination=0.03,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)

pipeline.fit(X)

predictions = pipeline.predict(X)
scores = pipeline.decision_function(X)

result = df[["vehicle_id", "timestamp"]].copy()
result["anomaly_flag"] = (predictions == -1).astype(int)
result["anomaly_score"] = (-scores).round(4)

output_path = os.path.join(BASE_DIR, "data", "vehicle_anomaly_scores.csv")
result.to_csv(output_path, index=False)

artifact = {
    "pipeline": pipeline,
    "features": features,
    "model_type": "IsolationForest",
    "contamination": 0.03,
}

joblib.dump(artifact, MODEL_PATH)

print("=" * 60)
print("AUTOMOTIVE ANOMALY DETECTION")
print("=" * 60)
print(f"Telemetry records: {len(df)}")
print(f"Features used: {len(features)}")
print(f"Anomalies detected: {result['anomaly_flag'].sum()}")
print(
    f"Anomaly rate: "
    f"{result['anomaly_flag'].mean() * 100:.2f}%"
)
print()
print(f"Scores saved to: {output_path}")
print(f"Model saved to: {MODEL_PATH}")
print("=" * 60)
