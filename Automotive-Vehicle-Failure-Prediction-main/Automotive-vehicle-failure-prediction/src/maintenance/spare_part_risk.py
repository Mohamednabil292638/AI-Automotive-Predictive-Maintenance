import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "vehicle_risk_prioritization.csv",
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "spare_part_risk_prioritization.csv",
)


df = pd.read_csv(INPUT_PATH)


PART_MAPPING = {
    "Engine": {
        "spare_part_category": "Engine & Thermal System",
        "priority_parts": "Engine cooling components / oil system components",
        "service_action": "Inspect engine thermal and lubrication system",
    },
    "Brake": {
        "spare_part_category": "Brake System",
        "priority_parts": "Brake pads / brake fluid system / brake components",
        "service_action": "Inspect brake wear, fluid level and brake temperature",
    },
    "Battery": {
        "spare_part_category": "Battery & Electrical System",
        "priority_parts": "Battery / alternator / electrical charging components",
        "service_action": "Inspect battery health and charging system",
    },
}


def map_part_category(component):
    return PART_MAPPING.get(
        component,
        {
            "spare_part_category": "General Vehicle System",
            "priority_parts": "Diagnostic inspection required",
            "service_action": "Perform vehicle diagnostic inspection",
        },
    )


mapped = df["priority_component"].apply(map_part_category)

df["spare_part_category"] = mapped.apply(
    lambda x: x["spare_part_category"]
)

df["priority_parts"] = mapped.apply(
    lambda x: x["priority_parts"]
)

df["service_action"] = mapped.apply(
    lambda x: x["service_action"]
)


def determine_parts_priority(row):
    if row["risk_level"] == "Critical":
        return "P1 - Immediate"
    if row["risk_level"] == "High":
        return "P2 - High"
    if row["risk_level"] == "Moderate":
        return "P3 - Monitor"
    return "P4 - Routine"


df["parts_priority"] = df.apply(
    determine_parts_priority,
    axis=1,
)

df["spare_part_risk_score"] = (
    df["vehicle_risk_score"] * 0.7
    + (100 - df["overall_health_score"]) * 0.3
).round(2)


columns = [
    "vehicle_id",
    "timestamp",
    "vehicle_risk_score",
    "risk_level",
    "priority_component",
    "overall_health_score",
    "spare_part_risk_score",
    "parts_priority",
    "spare_part_category",
    "priority_parts",
    "service_action",
]

df[columns].to_csv(OUTPUT_PATH, index=False)


print("=" * 60)
print("SPARE-PART RISK & MAINTENANCE PRIORITIZATION")
print("=" * 60)
print(f"Records analyzed: {len(df)}")
print(f"Vehicles: {df['vehicle_id'].nunique()}")
print()

print("Parts Priority Distribution:")
print(
    df["parts_priority"]
    .value_counts()
    .sort_index()
)

print()
print("Highest Priority Spare-Part Signals:")
print(
    df[
        [
            "vehicle_id",
            "timestamp",
            "spare_part_risk_score",
            "parts_priority",
            "priority_component",
            "spare_part_category",
            "service_action",
        ]
    ]
    .sort_values("spare_part_risk_score", ascending=False)
    .head(10)
    .to_string(index=False)
)

print()
print(f"Saved to: {OUTPUT_PATH}")
print("=" * 60)
