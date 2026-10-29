import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_telemetry_data.csv")

sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from features.component_health import calculate_component_health

df = pd.read_csv(DATA_PATH)
health_df = calculate_component_health(df)

output_columns = [
    "vehicle_id",
    "timestamp",
    "engine_health_score",
    "brake_health_score",
    "battery_health_score",
    "overall_health_score",
]

available_columns = [c for c in output_columns if c in health_df.columns]

output_path = os.path.join(BASE_DIR, "data", "vehicle_component_health.csv")
health_df[available_columns].to_csv(output_path, index=False)

print("=" * 60)
print("COMPONENT HEALTH ANALYSIS")
print("=" * 60)
print(f"Vehicles analyzed: {health_df['vehicle_id'].nunique()}")
print(f"Telemetry records: {len(health_df)}")
print()
print("Average Health Scores:")
print(f"Engine:   {health_df['engine_health_score'].mean():.1f}/100")
print(f"Brake:    {health_df['brake_health_score'].mean():.1f}/100")
print(f"Battery:  {health_df['battery_health_score'].mean():.1f}/100")
print(f"Overall:  {health_df['overall_health_score'].mean():.1f}/100")
print()
print(f"Saved to: {output_path}")
print("=" * 60)
