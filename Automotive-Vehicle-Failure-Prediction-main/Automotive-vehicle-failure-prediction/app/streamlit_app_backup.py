import os
import sys
import joblib
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_telemetry_data.csv")
RISK_PATH = os.path.join(BASE_DIR, "data", "spare_part_risk_prioritization.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "failure_risk_model.joblib")

sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from features.component_health import calculate_component_health

st.set_page_config(
    page_title="Automotive Predictive Maintenance",
    page_icon="??",
    layout="wide",
)

@st.cache_data
def load_data():
    telemetry = pd.read_csv(DATA_PATH)
    risk = pd.read_csv(RISK_PATH)

    telemetry["timestamp"] = pd.to_datetime(
        telemetry["timestamp"], errors="coerce"
    )
    risk["timestamp"] = pd.to_datetime(
        risk["timestamp"], errors="coerce"
    )

    telemetry = calculate_component_health(telemetry)

    return telemetry, risk


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


telemetry, risk = load_data()
artifact = load_model()

st.title("Automotive Predictive Maintenance & Vehicle Health")

st.caption(
    "AI-powered prototype for automotive telemetry, anomaly detection, "
    "component health and maintenance prioritization."
)

# Fleet Overview
total_vehicles = risk["vehicle_id"].nunique()
critical_count = int((risk["risk_level"] == "Critical").sum())
high_count = int((risk["risk_level"] == "High").sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicles", total_vehicles)
col2.metric("Telemetry Records", len(telemetry))
col3.metric("Critical Risk Records", critical_count)
col4.metric("High Risk Records", high_count)

st.divider()

# Vehicle Risk Analysis
st.subheader("Vehicle Risk Analysis")

vehicle_options = sorted(
    risk["vehicle_id"].dropna().unique()
)

selected_vehicle = st.selectbox(
    "Select Vehicle",
    vehicle_options,
)

vehicle_risk = risk[
    risk["vehicle_id"] == selected_vehicle
].copy()

vehicle_telemetry = telemetry[
    telemetry["vehicle_id"] == selected_vehicle
].copy()

latest = (
    vehicle_risk
    .sort_values("timestamp")
    .iloc[-1]
)

latest_telemetry = (
    vehicle_telemetry
    .sort_values("timestamp")
    .iloc[-1]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Risk Score",
    f"{latest['vehicle_risk_score']:.1f}/100",
)

col2.metric(
    "Risk Level",
    str(latest["risk_level"]),
)

col3.metric(
    "Overall Health",
    f"{latest['overall_health_score']:.1f}/100",
)

col4.metric(
    "Priority Component",
    str(latest["priority_component"]),
)

st.divider()

# Component Health
st.subheader("Component Health")

health_data = pd.DataFrame(
    {
        "Component": [
            "Engine",
            "Brake",
            "Battery",
        ],
        "Health Score": [
            float(latest_telemetry["engine_health_score"]),
            float(latest_telemetry["brake_health_score"]),
            float(latest_telemetry["battery_health_score"]),
        ],
    }
)

st.bar_chart(
    health_data,
    x="Component",
    y="Health Score",
    y_label="Health Score (0-100)",
    height=320,
)

health_col1, health_col2, health_col3 = st.columns(3)

health_col1.metric(
    "Engine Health",
    f"{latest_telemetry['engine_health_score']:.1f}/100",
)

health_col2.metric(
    "Brake Health",
    f"{latest_telemetry['brake_health_score']:.1f}/100",
)

health_col3.metric(
    "Battery Health",
    f"{latest_telemetry['battery_health_score']:.1f}/100",
)

st.divider()

# Maintenance Recommendation
st.subheader("Maintenance Recommendation")

st.info(
    f"Recommended action: {latest['service_action']}\n\n"
    f"Priority component: {latest['priority_component']}\n\n"
    f"Spare-part category: {latest['spare_part_category']}\n\n"
    f"Priority parts: {latest['priority_parts']}\n\n"
    f"Parts priority: {latest['parts_priority']}"
)

st.divider()

# Highest Risk Records
st.subheader("Highest-Risk Vehicle Records")

ranking_columns = [
    "vehicle_id",
    "timestamp",
    "vehicle_risk_score",
    "risk_level",
    "priority_component",
    "parts_priority",
]

ranking = (
    risk[ranking_columns]
    .sort_values(
        "vehicle_risk_score",
        ascending=False,
    )
    .head(20)
)

st.dataframe(
    ranking,
    width="stretch",
    hide_index=True,
)

st.divider()

# Risk Distribution
st.subheader("Risk Distribution")

risk_distribution = (
    risk["risk_level"]
    .value_counts()
    .reindex(
        ["Low", "Moderate", "High", "Critical"],
        fill_value=0,
    )
)

risk_distribution_data = pd.DataFrame(
    {
        "Risk Level": risk_distribution.index,
        "Records": risk_distribution.values,
    }
)

st.bar_chart(
    risk_distribution_data,
    x="Risk Level",
    y="Records",
    y_label="Telemetry Records",
    height=320,
)

st.divider()

st.caption(
    "Research prototype based on synthetic automotive telemetry. "
    "Health scores, risk thresholds and spare-part mappings are "
    "analytical prototypes and are not OEM-certified recommendations."
)


