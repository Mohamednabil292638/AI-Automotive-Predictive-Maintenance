from pathlib import Path
import json
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Automotive Predictive Maintenance Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
EVALUATION_FILE = MODEL_DIR / "model_evaluation.json"

RISK_FILE = DATA_DIR / "vehicle_risk_prioritization.csv"
HEALTH_FILE = DATA_DIR / "vehicle_component_health.csv"
ANOMALY_FILE = DATA_DIR / "vehicle_anomaly_scores.csv"
TELEMETRY_FILE = DATA_DIR / "synthetic_telemetry_data.csv"

st.markdown("""
<style>

/* ============================================================
   PREMIUM AUTOMOTIVE INTELLIGENCE UI
   Mercedes-Benz-inspired luxury cockpit aesthetic
   ============================================================ */

:root {
    --luxury-bg: #080a0d;
    --luxury-panel: #111419;
    --luxury-panel-2: #171a20;
    --luxury-border: rgba(255,255,255,0.10);
    --luxury-text: #f5f5f5;
    --luxury-muted: #9ca3af;
    --luxury-silver: #d9dde3;
    --luxury-red: #e11d2e;
}

/* Main application */
.stApp {
    background:
        radial-gradient(circle at 82% 8%, rgba(255,255,255,0.055), transparent 22%),
        radial-gradient(circle at 12% 25%, rgba(255,255,255,0.025), transparent 25%),
        linear-gradient(135deg, #060709 0%, #0b0d11 45%, #08090c 100%);
    color: var(--luxury-text);
}

/* Main content */
.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #090b0e 0%, #0e1014 50%, #08090c 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #e8eaed !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #15181d !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    border-radius: 10px !important;
}

/* Header / hero */
.auto-hero {
    position: relative;
    overflow: hidden;
    min-height: 230px;
    padding: 34px 38px;
    margin-bottom: 24px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.11);
    background:
        radial-gradient(circle at 88% 20%, rgba(255,255,255,0.10), transparent 20%),
        linear-gradient(120deg, #0b0d10 0%, #15181d 55%, #0b0d10 100%);
    box-shadow:
        0 25px 70px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.06);
}

.auto-hero:after {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    right: -110px;
    top: -170px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
        0 0 0 35px rgba(255,255,255,0.015),
        0 0 0 70px rgba(255,255,255,0.01);
}

.auto-kicker {
    color: #aeb4bd;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    font-size: 0.70rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.auto-title {
    font-size: clamp(2rem, 4vw, 3.45rem);
    line-height: 1.02;
    font-weight: 800;
    letter-spacing: -0.045em;
    color: #ffffff;
    margin-bottom: 12px;
}

.auto-title span {
    color: #cdd2d9;
}

.auto-subtitle {
    max-width: 720px;
    color: #a7adb7;
    font-size: 0.96rem;
    line-height: 1.65;
}

.auto-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 20px;
    padding: 7px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.11);
    background: rgba(255,255,255,0.045);
    color: #d7dbe1;
    font-size: 0.75rem;
}

.auto-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 12px rgba(34,197,94,0.65);
}

/* Section headings */
.section-title {
    font-size: 1.25rem;
    font-weight: 750;
    color: #f3f4f6;
    margin-top: 18px;
    margin-bottom: 10px;
}

.section-caption {
    color: #8f96a1;
    font-size: 0.82rem;
}

/* Metric cards */
[data-testid="stMetric"] {
    background:
        linear-gradient(145deg, rgba(255,255,255,0.055), rgba(255,255,255,0.018));
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 15px;
    padding: 17px 18px;
    min-height: 112px;
    box-shadow:
        0 12px 30px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.035);
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(255,255,255,0.18);
    box-shadow: 0 18px 38px rgba(0,0,0,0.30);
}

[data-testid="stMetricLabel"] {
    color: #9299a4 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.10em;
}

[data-testid="stMetricValue"] {
    color: #f7f7f8 !important;
    font-size: 1.65rem !important;
    font-weight: 760 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    background: rgba(255,255,255,0.025);
    padding: 5px;
    border-radius: 13px;
    border: 1px solid rgba(255,255,255,0.07);
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    padding: 0 17px;
    color: #8f96a1;
    border-radius: 9px;
    font-size: 0.82rem;
}

.stTabs [aria-selected="true"] {
    background: #e9ebee !important;
    color: #101216 !important;
    font-weight: 700;
}

/* Charts / dataframes */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Select boxes */
.stSelectbox label,
.stMultiSelect label {
    color: #aeb4bd !important;
    font-size: 0.78rem !important;
    font-weight: 650 !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.12);
    background: linear-gradient(135deg, #e7e9ec, #bfc4ca);
    color: #0b0d10;
    font-weight: 750;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 13px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* Markdown */
p, li {
    color: #c2c7cf;
}

h1, h2, h3, h4 {
    color: #f4f5f6 !important;
}

/* Footer */
.auto-footer {
    margin-top: 42px;
    padding-top: 18px;
    border-top: 1px solid rgba(255,255,255,0.08);
    color: #6f7680;
    font-size: 0.72rem;
    text-align: center;
    letter-spacing: 0.04em;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .auto-hero {
        padding: 25px;
        min-height: 200px;
    }

    .auto-title {
        font-size: 2rem;
    }
}

</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    risk = pd.read_csv(RISK_FILE)
    health = pd.read_csv(HEALTH_FILE)
    anomaly = pd.read_csv(ANOMALY_FILE)
    telemetry = pd.read_csv(TELEMETRY_FILE)

    for df in [risk, health, anomaly, telemetry]:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return risk, health, anomaly, telemetry


risk, health, anomaly, telemetry = load_data()

# Load the latest model evaluation generated by train_failure_model.py
@st.cache_data
def load_model_evaluation():
    if not EVALUATION_FILE.exists():
        return {}
    try:
        with open(EVALUATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

model_evaluation = load_model_evaluation()
model_metrics = model_evaluation.get("metrics", {})

vehicle_list = sorted(risk["vehicle_id"].dropna().unique())

st.sidebar.title("Vehicle Intelligence")
selected_vehicle = st.sidebar.selectbox("Select Vehicle", vehicle_list)

st.sidebar.markdown("---")
st.sidebar.markdown("### System Scope")
st.sidebar.markdown("""
- Predictive maintenance
- Sensor anomaly detection
- Component health
- Failure-risk scoring
- Spare-part prioritization
""")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Research prototype using synthetic automotive telemetry. "
    "Not OEM-certified maintenance advice."
)

# ------------------------------------------------------------
# SELECTED VEHICLE STATE
# Rebuild all vehicle-specific datasets from the current
# sidebar selection on every Streamlit rerun.
# ------------------------------------------------------------
vehicle_risk = (
    risk.loc[risk["vehicle_id"].eq(selected_vehicle)]
    .copy()
    .sort_values("timestamp")
    .reset_index(drop=True)
)

vehicle_health = (
    health.loc[health["vehicle_id"].eq(selected_vehicle)]
    .copy()
    .sort_values("timestamp")
    .reset_index(drop=True)
)

vehicle_anomaly = (
    anomaly.loc[anomaly["vehicle_id"].eq(selected_vehicle)]
    .copy()
    .sort_values("timestamp")
    .reset_index(drop=True)
)

vehicle_telemetry = (
    telemetry.loc[telemetry["vehicle_id"].eq(selected_vehicle)]
    .copy()
    .sort_values("timestamp")
    .reset_index(drop=True)
)


st.markdown(f"""
<div class="auto-hero">
    <div class="auto-kicker">AUTOMOTIVE INTELLIGENCE • AI • PREDICTIVE AFTERSALES</div>
    <div class="auto-title">Vehicle Intelligence<br><span>Command Center</span></div>
    <div class="auto-subtitle">
        AI-driven vehicle health, anomaly detection, failure-risk analytics
        and predictive maintenance intelligence for connected automotive systems.
    </div>
    <div class="auto-status">
        <span class="auto-status-dot"></span>
        LIVE ANALYTICS - {selected_vehicle}
    </div>
</div>
""", unsafe_allow_html=True)

if vehicle_risk.empty or vehicle_telemetry.empty:
    st.error(f"No data available for selected vehicle: {selected_vehicle}")
    st.stop()

latest = vehicle_risk.iloc[-1]
latest_health = vehicle_health.iloc[-1] if not vehicle_health.empty else None
latest_anomaly = vehicle_anomaly.iloc[-1] if not vehicle_anomaly.empty else None
latest_telemetry = vehicle_telemetry.iloc[-1]

st.title("🚗 Automotive Predictive Maintenance Intelligence")
st.caption(
    "AI-driven vehicle health, anomaly detection, failure-risk analytics "
    "and spare-part maintenance prioritization"
)

tab_fleet, tab_vehicle, tab_diag, tab_maintenance, tab_model = st.tabs([
    "📊 Fleet Command",
    "🚘 Vehicle Health",
    "🔍 Sensor Diagnostics",
    "🛠 Maintenance Intelligence",
    "🧠 Model & Innovation",
])


# ============================================================
# FLEET COMMAND
# ============================================================
with tab_fleet:

    st.subheader("Fleet Command Center")

    total_vehicles = risk["vehicle_id"].nunique()
    telemetry_records = len(telemetry)
    critical_count = int((risk["risk_level"] == "Critical").sum())
    high_count = int((risk["risk_level"] == "High").sum())
    anomaly_count = int(risk["anomaly_flag"].sum())

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Vehicles Monitored", f"{total_vehicles:,}")
    c2.metric("Telemetry Records", f"{telemetry_records:,}")
    c3.metric("Critical Records", f"{critical_count:,}")
    c4.metric("High-Risk Records", f"{high_count:,}")
    c5.metric("Detected Anomalies", f"{anomaly_count:,}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Fleet Risk Distribution")
        distribution = (
            risk["risk_level"]
            .value_counts()
            .reindex(["Critical", "High", "Moderate", "Low"])
            .fillna(0)
            .astype(int)
            .rename_axis("Risk Level")
            .reset_index(name="Records")
        )
        st.bar_chart(distribution, x="Risk Level", y="Records", width="stretch")

    with col2:
        st.subheader("Maintenance Priority")

        priority = pd.Series(
            np.select(
                [
                    risk["risk_level"].eq("Critical"),
                    risk["risk_level"].eq("High"),
                    risk["risk_level"].eq("Moderate"),
                ],
                ["P1 - Immediate", "P2 - High", "P3 - Monitor"],
                default="P4 - Routine",
            )
        )

        priority_df = (
            priority.value_counts()
            .reindex(
                ["P1 - Immediate", "P2 - High", "P3 - Monitor", "P4 - Routine"]
            )
            .fillna(0)
            .astype(int)
            .rename_axis("Priority")
            .reset_index(name="Records")
        )

        st.bar_chart(priority_df, x="Priority", y="Records", width="stretch")

    st.markdown("---")
    st.subheader("Highest-Risk Vehicle Records")

    highest = risk.sort_values("vehicle_risk_score", ascending=False).head(15).copy()

    highest["failure_probability"] = (
        highest["failure_probability"] * 100
    ).round(1)

    display_cols = [
        "vehicle_id",
        "timestamp",
        "vehicle_risk_score",
        "risk_level",
        "priority_component",
        "failure_probability",
        "anomaly_flag",
    ]

    highest["vehicle_risk_score"] = highest["vehicle_risk_score"].round(2)

    st.dataframe(
        highest[display_cols],
        width="stretch",
        hide_index=True,
    )


# ============================================================
# VEHICLE HEALTH
# ============================================================
with tab_vehicle:

    st.subheader(f"Vehicle Digital Health Profile — {selected_vehicle}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Vehicle Risk",
        f"{latest['vehicle_risk_score']:.1f}/100"
    )

    c2.metric(
        "Risk Level",
        latest["risk_level"]
    )

    c3.metric(
        "Overall Health",
        f"{latest['overall_health_score']:.1f}/100"
    )

    c4.metric(
        "Failure Probability",
        f"{latest['failure_probability'] * 100:.1f}%"
    )

    st.markdown("---")

    st.subheader("Component Health")

    component_df = pd.DataFrame({
        "Component": [
            "Engine",
            "Brake",
            "Battery",
        ],
        "Health Score": [
            latest["engine_health_score"],
            latest["brake_health_score"],
            latest["battery_health_score"],
        ],
    })

    st.bar_chart(
        component_df,
        x="Component",
        y="Health Score",
        width="stretch",
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Engine Health",
        f"{latest['engine_health_score']:.1f}/100"
    )

    c2.metric(
        "Brake Health",
        f"{latest['brake_health_score']:.1f}/100"
    )

    c3.metric(
        "Battery Health",
        f"{latest['battery_health_score']:.1f}/100"
    )

    st.markdown("---")
    st.subheader("Risk Interpretation")

    component_scores = {
        "Engine": latest["engine_health_score"],
        "Brake": latest["brake_health_score"],
        "Battery": latest["battery_health_score"],
    }

    primary_component = min(component_scores, key=component_scores.get)
    primary_score = component_scores[primary_component]

    st.info(
        f"Primary risk component: {primary_component}\n\n"
        f"Component health: {primary_score:.1f}/100\n\n"
        f"Vehicle risk: {latest['vehicle_risk_score']:.1f}/100 "
        f"({latest['risk_level']})\n\n"
        f"Failure probability: {latest['failure_probability'] * 100:.1f}%"
    )


# ============================================================
# SENSOR DIAGNOSTICS
# ============================================================
with tab_diag:

    st.subheader("Sensor Diagnostics & Anomaly Intelligence")

    st.caption(
        "Telemetry evidence from the selected vehicle. "
        "Signal status is calculated relative to the observed fleet distribution; "
        "it is not an OEM engineering limit."
    )

    anomaly_count_vehicle = int(vehicle_anomaly["anomaly_flag"].sum())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Vehicle Telemetry",
        f"{len(vehicle_telemetry):,}"
    )

    c2.metric(
        "Vehicle Anomalies",
        f"{anomaly_count_vehicle:,}"
    )

    c3.metric(
        "Fleet Anomalies",
        f"{anomaly_count:,}"
    )

    c4.metric(
        "Vehicle Risk",
        f"{latest['vehicle_risk_score']:.1f}/100"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # SENSOR STATUS ENGINE
    # --------------------------------------------------------

    sensor_rules = {
        "Engine Temperature": ("engine_temp_c", "high"),
        "Oil Pressure": ("oil_pressure_psi", "low"),
        "Coolant Temperature": ("coolant_temp_c", "high"),
        "Engine Vibration": ("vibration_level", "high"),
        "Brake Pad Wear": ("brake_pad_wear_mm", "high"),
        "Brake Temperature": ("brake_temp_c", "high"),
        "Battery Voltage": ("battery_voltage_v", "low"),
        # Battery current is bidirectional (charging/discharging).
        # Do not classify negative current as inherently abnormal.
        # It is evaluated separately using fleet-relative magnitude.
        "Battery Temperature": ("battery_temp_c", "high"),
        "Battery Health": ("battery_health_percent", "low"),
        "Battery Charge": ("battery_charge_percent", "low"),
        "Alternator Output": ("alternator_output_v", "low"),
    }

    def signal_status(column, value, direction):

        series = telemetry[column].dropna()

        low_q = series.quantile(0.10)
        high_q = series.quantile(0.90)

        if direction == "high":
            if value >= high_q:
                return "Risk signal"
            elif value >= series.quantile(0.75):
                return "Watch"
            return "Normal"

        if direction == "low":
            if value <= low_q:
                return "Risk signal"
            elif value <= series.quantile(0.25):
                return "Watch"
            return "Normal"

        if direction == "bidirectional":
            magnitude = abs(value)
            magnitude_series = series.abs()

            magnitude_high = magnitude_series.quantile(0.90)
            magnitude_watch = magnitude_series.quantile(0.75)

            if magnitude >= magnitude_high:
                return "Risk signal"
            elif magnitude >= magnitude_watch:
                return "Watch"
            return "Normal"

        return "Normal"

    sensor_rows = []

    for name, (column, direction) in sensor_rules.items():

        value = float(latest_telemetry[column])

        status = signal_status(
            column,
            value,
            direction
        )

        sensor_rows.append({
            "Subsystem": (
                "Engine"
                if column in [
                    "engine_temp_c",
                    "oil_pressure_psi",
                    "coolant_temp_c",
                    "vibration_level",
                ]
                else
                "Brake"
                if column in [
                    "brake_pad_wear_mm",
                    "brake_temp_c",
                ]
                else
                "Electrical"
            ),
            "Signal": name,
            "Value": round(value, 2),
            "Unit": {
                "engine_temp_c": "°C",
                "oil_pressure_psi": "psi",
                "coolant_temp_c": "°C",
                "vibration_level": "index",
                "brake_pad_wear_mm": "mm",
                "brake_temp_c": "°C",
                "battery_voltage_v": "V",
                "battery_current_a": "A",
                "battery_temp_c": "°C",
                "battery_health_percent": "%",
                "battery_charge_percent": "%",
                "alternator_output_v": "V",
            }.get(column, ""),
            "Fleet-Relative Status": status,
        })

    sensor_status_df = pd.DataFrame(sensor_rows)

    # --------------------------------------------------------
    # ELECTRICAL SYSTEM INTELLIGENCE
    # --------------------------------------------------------
    st.markdown("---")
    st.subheader("Battery & Electrical Intelligence")

    st.caption(
        "Fleet-relative electrical diagnostics combining battery voltage, "
        "current direction, alternator output, charge level and battery health. "
        "These indicators are analytical signals from the available dataset, "
        "not OEM diagnostic thresholds."
    )

    battery_voltage = float(latest_telemetry["battery_voltage_v"])
    battery_current = float(latest_telemetry["battery_current_a"])
    alternator_output = float(latest_telemetry["alternator_output_v"])
    battery_charge = float(latest_telemetry["battery_charge_percent"])
    battery_health = float(latest_telemetry["battery_health_percent"])

    voltage_series = telemetry["battery_voltage_v"].dropna()
    alternator_series = telemetry["alternator_output_v"].dropna()
    charge_series = telemetry["battery_charge_percent"].dropna()
    health_series = telemetry["battery_health_percent"].dropna()

    voltage_low = voltage_series.quantile(0.10)
    alternator_low = alternator_series.quantile(0.10)
    charge_low = charge_series.quantile(0.10)
    health_low = health_series.quantile(0.10)

    electrical_signals = []

    if battery_voltage <= voltage_low:
        electrical_signals.append(
            "Low battery-voltage signal"
        )

    if alternator_output <= alternator_low:
        electrical_signals.append(
            "Low alternator-output signal"
        )

    if battery_charge <= charge_low:
        electrical_signals.append(
            "Low battery-charge signal"
        )

    if battery_health <= health_low:
        electrical_signals.append(
            "Low battery-health signal"
        )

    # Negative current is interpreted as a discharge direction,
    # not as an automatic fault.
    if battery_current < 0:
        electrical_signals.append(
            "Battery discharge direction observed"
        )

    if (
        battery_current < 0
        and battery_voltage <= voltage_low
        and battery_charge <= charge_low
    ):
        electrical_state = "Electrical risk"
        electrical_reason = (
            "Discharge direction is accompanied by relatively low "
            "battery voltage and charge level."
        )
    elif (
        battery_voltage <= voltage_low
        or alternator_output <= alternator_low
    ):
        electrical_state = "Charging-system watch"
        electrical_reason = (
            "One or more electrical measurements are relatively low "
            "compared with the observed fleet distribution."
        )
    elif battery_current < 0:
        electrical_state = "Discharge observed"
        electrical_reason = (
            "Negative battery current indicates discharge direction; "
            "this is not treated as a fault by itself."
        )
    else:
        electrical_state = "Stable electrical state"
        electrical_reason = (
            "No strong fleet-relative electrical risk combination "
            "was detected in the latest telemetry record."
        )

    ec1, ec2, ec3, ec4 = st.columns(4)

    ec1.metric(
        "Battery Voltage",
        f"{battery_voltage:.2f} V"
    )

    ec2.metric(
        "Battery Current",
        f"{battery_current:.2f} A"
    )

    ec3.metric(
        "Alternator Output",
        f"{alternator_output:.2f} V"
    )

    ec4.metric(
        "Battery Charge",
        f"{battery_charge:.1f}%"
    )

    if electrical_state == "Electrical risk":
        st.error(
            f"Electrical state: {electrical_state}\n\n"
            f"{electrical_reason}"
        )
    elif electrical_state == "Charging-system watch":
        st.warning(
            f"Electrical state: {electrical_state}\n\n"
            f"{electrical_reason}"
        )
    elif electrical_state == "Discharge observed":
        st.warning(
            f"Electrical state: {electrical_state}\n\n"
            f"{electrical_reason}"
        )
    else:
        st.success(
            f"Electrical state: {electrical_state}\n\n"
            f"{electrical_reason}"
        )

    if electrical_signals:
        st.write("Observed electrical signals:")
        for signal in electrical_signals:
            st.write(f"- {signal}")
    else:
        st.write("Observed electrical signals: none requiring attention.")

    st.caption(
        f"Battery health: {battery_health:.1f}% | "
        f"Fleet-relative lower voltage boundary: {voltage_low:.2f} V | "
        f"Fleet-relative lower charge boundary: {charge_low:.1f}%"
    )

    st.markdown("---")

    st.subheader("Current Sensor State")

    st.dataframe(
        sensor_status_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    # --------------------------------------------------------
    # ENGINE TRENDS
    # --------------------------------------------------------

    st.subheader("Powertrain Telemetry")

    engine_chart = (
        vehicle_telemetry[
            [
                "timestamp",
                "engine_temp_c",
                "coolant_temp_c",
                "oil_pressure_psi",
                "vibration_level",
            ]
        ]
        .copy()
        .sort_values("timestamp")
        .set_index("timestamp")
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Temperature Trend**")
        st.line_chart(
            engine_chart[
                ["engine_temp_c", "coolant_temp_c"]
            ],
            width="stretch",
        )

    with c2:
        st.markdown("**Oil Pressure / Vibration Trend**")
        st.line_chart(
            engine_chart[
                ["oil_pressure_psi", "vibration_level"]
            ],
            width="stretch",
        )

    st.markdown("---")

    # --------------------------------------------------------
    # BRAKE + ELECTRICAL
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Brake System Telemetry")

        brake_chart = (
            vehicle_telemetry[
                [
                    "timestamp",
                    "brake_pad_wear_mm",
                    "brake_temp_c",
                    "brake_fluid_level_psi",
                ]
            ]
            .copy()
            .sort_values("timestamp")
            .set_index("timestamp")
        )

        st.line_chart(
            brake_chart,
            width="stretch",
        )

        st.caption(
            "Brake-pad wear, brake temperature and brake-fluid signal "
            "shown across the selected vehicle's telemetry history."
        )

    with c2:

        st.subheader("Electrical System Telemetry")

        electrical_chart = (
            vehicle_telemetry[
                [
                    "timestamp",
                    "battery_voltage_v",
                    "battery_current_a",
                    "alternator_output_v",
                    "battery_charge_percent",
                ]
            ]
            .copy()
            .sort_values("timestamp")
            .set_index("timestamp")
        )

        st.line_chart(
            electrical_chart,
            width="stretch",
        )

        st.caption(
            "Battery voltage/current, alternator output and charge level "
            "shown across the selected vehicle's telemetry history."
        )

    st.markdown("---")

    # --------------------------------------------------------
    # FAILURE EVIDENCE
    # --------------------------------------------------------

    st.subheader("Failure Evidence & Risk Drivers")

    selected_failures = vehicle_telemetry[
        vehicle_telemetry["failure_type"].notna()
        & (
            vehicle_telemetry["failure_type"]
            .astype(str)
            .str.lower()
            != "no failure"
        )
    ].copy()

    if len(selected_failures) > 0:

        st.warning(
            f"{len(selected_failures)} failure event(s) are present "
            f"in this vehicle's telemetry history."
        )

        failure_cols = [
            "timestamp",
            "failure_type",
            "engine_temp_c",
            "oil_pressure_psi",
            "vibration_level",
            "brake_pad_wear_mm",
            "brake_temp_c",
            "battery_voltage_v",
            "battery_current_a",
            "battery_health_percent",
        ]

        st.dataframe(
            selected_failures[failure_cols].sort_values(
                "timestamp",
                ascending=False
            ),
            width="stretch",
            hide_index=True,
        )

    else:

        st.success(
            "No labeled failure event is present in the selected "
            "vehicle's available telemetry history."
        )

    # ============================================================
    # EXPLAINABLE RISK EVIDENCE
    # ============================================================
    st.markdown("### Explainable Risk Evidence")
    st.caption(
        "This section decomposes the vehicle risk score into model risk, "
        "anomaly risk and component-health risk, then links current sensor "
        "evidence to the primary maintenance component."
    )

    failure_contribution = float(latest["failure_probability"]) * 100 * 0.50
    anomaly_contribution = float(latest["anomaly_risk"]) * 0.25
    health_contribution = float(latest["health_risk"]) * 0.25

    risk_decomposition = pd.DataFrame({
        "Risk Source": [
            "Failure-model risk",
            "Anomaly risk",
            "Component-health risk"
        ],
        "Contribution": [
            failure_contribution,
            anomaly_contribution,
            health_contribution
        ]
    })

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("#### Risk Score Decomposition")
        st.bar_chart(
            risk_decomposition.set_index("Risk Source"),
            y="Contribution"
        )
        st.caption(
            "Vehicle Risk = 50% failure probability + 25% anomaly risk "
            "+ 25% health risk."
        )

    with c2:
        st.markdown("#### Engineering Risk Summary")

        summary_rows = [
            {
                "Evidence": "Failure probability",
                "Value": f"{latest['failure_probability'] * 100:.1f}%",
                "Interpretation": "Model-estimated failure-event risk"
            },
            {
                "Evidence": "Anomaly risk",
                "Value": f"{latest['anomaly_risk'] * 100:.1f}%",
                "Interpretation": "Isolation Forest anomaly signal"
            },
            {
                "Evidence": "Overall health",
                "Value": f"{latest['overall_health_score']:.1f}/100",
                "Interpretation": "Component-health aggregation"
            },
            {
                "Evidence": "Primary component",
                "Value": str(latest["priority_component"]),
                "Interpretation": "Maintenance prioritization target"
            }
        ]

        st.dataframe(
            pd.DataFrame(summary_rows),
            hide_index=True,
            width="stretch"
        )

    # Current sensor evidence supporting the risk interpretation.
    evidence_rules = {
        "engine_temp_c": (
            "Engine",
            "Upper-tail thermal signal",
            "Elevated engine temperature can indicate thermal stress in this synthetic fleet."
        ),
        "coolant_temp_c": (
            "Engine",
            "Upper-tail cooling signal",
            "Elevated coolant temperature is consistent with thermal-system stress."
        ),
        "oil_pressure_psi": (
            "Engine",
            "Lower-tail lubrication signal",
            "Low oil pressure appears in observed low-oil-pressure and overheat events."
        ),
        "vibration_level": (
            "Engine",
            "Upper-tail vibration signal",
            "Elevated vibration is consistent with the excessive-vibration events present in the dataset."
        ),
        "brake_pad_wear_mm": (
            "Brake",
            "High wear signal",
            "High brake-pad wear is consistent with observed brake-pad-worn events."
        ),
        "brake_temp_c": (
            "Brake",
            "Upper-tail thermal signal",
            "High brake temperature is consistent with observed brake-overheat events."
        ),
        "brake_fluid_level_psi": (
            "Brake",
            "Lower-tail fluid signal",
            "Low brake-fluid readings are consistent with observed low-brake-fluid events."
        ),
        "battery_voltage_v": (
            "Battery",
            "Lower-tail voltage signal",
            "Low battery voltage appears in observed battery-dead, battery-drain and low-voltage events."
        ),
        "battery_current_a": (
            "Battery",
            "Negative-current signal",
            "Strong negative battery current appears in observed battery-dead and battery-drain events."
        ),
        "battery_charge_percent": (
            "Battery",
            "Lower-tail charge signal",
            "Low charge can increase the electrical-system maintenance priority."
        ),
        "battery_health_percent": (
            "Battery",
            "Lower-tail health signal",
            "Lower battery health contributes to the component-health risk."
        ),
        "alternator_output_v": (
            "Battery",
            "Charging-system signal",
            "Low alternator output can indicate charging-system attention is required."
        )
    }

    evidence_rows = []

    for _, rule in sensor_rules.items():
        column = rule[0]

        if column not in latest.index or column not in telemetry.columns:
            continue

        value = latest[column]
        series = telemetry[column].dropna()

        if series.empty:
            continue

        q10 = series.quantile(0.10)
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        q90 = series.quantile(0.90)

        direction = rule[1]

        if direction == "high":
            if value >= q90:
                status = "HIGH CONCERN"
            elif value >= q75:
                status = "WATCH"
            else:
                continue

        elif direction == "low":
            if value <= q10:
                status = "HIGH CONCERN"
            elif value <= q25:
                status = "WATCH"
            else:
                continue

        else:
            continue

        if column not in evidence_rules:
            continue

        component, evidence_type, rationale = evidence_rules[column]

        evidence_rows.append({
            "Component": component,
            "Signal": column,
            "Current Value": round(float(value), 3),
            "Evidence": evidence_type,
            "Status": status,
            "Engineering Interpretation": rationale
        })

    if evidence_rows:
        evidence_df = pd.DataFrame(evidence_rows)

        priority = str(latest["priority_component"]).lower()

        evidence_df["Priority"] = evidence_df["Component"].apply(
            lambda x: "PRIMARY" if str(x).lower() in priority else "SUPPORTING"
        )

        evidence_df = evidence_df.sort_values(
            ["Priority", "Status"],
            ascending=[True, True]
        )

        st.markdown("#### Current Sensor Evidence")

        st.dataframe(
            evidence_df,
            hide_index=True,
            width="stretch"
        )

        st.info(
            "Interpretation note: sensor evidence is fleet-relative and "
            "supports the analytical risk decision. It is not an OEM diagnostic "
            "threshold and does not establish causality."
        )
    else:
        st.success(
            "No strong fleet-relative sensor evidence was detected for the selected vehicle."
        )

    st.markdown("#### Risk-to-Maintenance Chain")

    chain = [
        "Current telemetry",
        "Sensor deviation / anomaly",
        "Component health",
        "Failure-event risk",
        "Vehicle risk score",
        "Primary component",
        "Maintenance priority"
    ]

    chain_cols = st.columns(len(chain))

    for i, item in enumerate(chain):
        with chain_cols[i]:
            st.markdown(
                f"**{i + 1}.** {item}"
            )

    st.caption(
        "This chain is the project's explainability layer: it connects "
        "vehicle telemetry to an actionable maintenance-prioritization signal."
    )

    st.info(
        "Anomaly detection uses Isolation Forest as an unsupervised "
        "telemetry-anomaly prototype. Sensor statuses above are "
        "fleet-relative diagnostics and should not be interpreted "
        "as OEM safety thresholds."
    )


# ============================================================
# MAINTENANCE INTELLIGENCE
# ============================================================
with tab_maintenance:

    st.subheader("Maintenance & Spare-Part Intelligence")

    priority_component = latest["priority_component"]

    priority_map = {
        "Critical": "P1 - Immediate",
        "High": "P2 - High",
        "Moderate": "P3 - Monitor",
        "Low": "P4 - Routine",
    }

    parts_priority = priority_map.get(
        latest["risk_level"],
        "P4 - Routine"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Priority Component",
        priority_component
    )

    c2.metric(
        "Parts Priority",
        parts_priority
    )

    c3.metric(
        "Overall Health",
        f"{latest['overall_health_score']:.1f}/100"
    )

    st.markdown("---")

    st.subheader("Recommended Engineering Action")

    st.success(
        str(latest["recommended_action"])
    )

    st.markdown("---")

    st.subheader("Decision Logic")

    logic_df = pd.DataFrame({
        "Signal": [
            "Failure Probability",
            "Anomaly Risk",
            "Health Risk",
            "Vehicle Risk Score",
            "Priority Component",
        ],
        "Value": [
            f"{latest['failure_probability'] * 100:.1f}%",
            f"{latest['anomaly_risk']:.1f}/100",
            f"{latest['health_risk']:.1f}/100",
            f"{latest['vehicle_risk_score']:.1f}/100",
            priority_component,
        ],
    })

    st.dataframe(
        logic_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    st.subheader("Spare-Part Risk Concept")

    spare_part_map = {
        "Engine": [
            "Engine cooling components",
            "Oil-system components",
            "Thermal-management components",
        ],
        "Brake": [
            "Brake-pad components",
            "Brake-fluid system components",
            "Brake thermal-management components",
        ],
        "Battery": [
            "Battery / energy-storage components",
            "Charging-system components",
            "Electrical power-management components",
        ],
    }

    st.markdown(
        "Telemetry → Failure Risk → Anomaly → Component Health → "
        "Vehicle Risk → Maintenance Priority → Spare-Part Risk Signal"
    )

    st.markdown(
        f"**Priority subsystem: {priority_component}**"
    )

    for part in spare_part_map.get(priority_component, []):
        st.markdown(f"- {part}")

    st.caption(
        "These are analytical spare-part categories, not OEM-specific "
        "part numbers or validated replacement recommendations."
    )



# ============================================================
# SPARE-PART INTELLIGENCE
# ============================================================

with tab_maintenance:

    st.markdown("---")
    st.subheader("Predictive Spare-Part Intelligence")

    st.caption(
        "Analytical component-to-part prioritization derived from vehicle "
        "risk, component health and telemetry evidence. Part categories are "
        "generic engineering categories and are not OEM part numbers."
    )

    component_health = {
        "Engine": float(latest["engine_health_score"]),
        "Brake": float(latest["brake_health_score"]),
        "Battery": float(latest["battery_health_score"]),
    }

    component_priority = str(latest["priority_component"])

    component_mapping = {
        "Engine": {
            "system": "Engine & Thermal System",
            "parts": "Cooling-system components, lubrication-related components",
            "action": "Inspect engine thermal and lubrication conditions",
        },
        "Brake": {
            "system": "Brake System",
            "parts": "Brake pads, brake-fluid-related components",
            "action": "Inspect braking wear, temperature and fluid condition",
        },
        "Battery": {
            "system": "Battery & Electrical System",
            "parts": "Battery, charging-system components",
            "action": "Inspect battery condition and charging-system performance",
        },
    }

    mapping = component_mapping.get(
        component_priority,
        {
            "system": "Vehicle System",
            "parts": "Component-specific service parts",
            "action": "Perform engineering inspection",
        }
    )

    vehicle_risk_score = float(latest["vehicle_risk_score"])

    if vehicle_risk_score > 80:
        spare_priority = "P1 — Immediate inspection"
    elif vehicle_risk_score > 60:
        spare_priority = "P2 — High priority"
    elif vehicle_risk_score > 30:
        spare_priority = "P3 — Planned maintenance"
    else:
        spare_priority = "P4 — Monitor"

    sp1, sp2, sp3 = st.columns(3)

    sp1.metric(
        "Priority Component",
        component_priority
    )

    sp2.metric(
        "Spare-Part Priority",
        spare_priority
    )

    sp3.metric(
        "Vehicle Risk",
        f"{vehicle_risk_score:.1f}/100"
    )

    st.markdown("### Recommended Spare-Part Category")

    spare_part_rows = [
        {
            "Engineering System": mapping["system"],
            "Priority Component": component_priority,
            "Candidate Part Category": mapping["parts"],
            "Priority": spare_priority,
            "Recommended Action": mapping["action"],
        }
    ]

    st.dataframe(
        pd.DataFrame(spare_part_rows),
        hide_index=True,
        width="stretch",
    )

    st.markdown("### Component Health Ranking")

    health_rows = []

    for component, score in sorted(
        component_health.items(),
        key=lambda item: item[1]
    ):
        if score <= 30:
            condition = "Critical"
        elif score <= 60:
            condition = "Attention"
        elif score <= 80:
            condition = "Watch"
        else:
            condition = "Healthy"

        health_rows.append({
            "Component": component,
            "Health Score": round(score, 1),
            "Condition": condition,
        })

    st.dataframe(
        pd.DataFrame(health_rows),
        hide_index=True,
        width="stretch",
    )

    st.info(
        f"Maintenance chain: {component_priority} → "
        f"{mapping['system']} → {mapping['parts']} → "
        f"{spare_priority} → {mapping['action']}."
    )

# ============================================================
# MODEL & INNOVATION
# ============================================================
with tab_model:

    st.subheader("Model Intelligence & Innovation Architecture")

    st.subheader("ML Model Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("ROC-AUC", f"{model_metrics.get('roc_auc', 0):.3f}")
    c2.metric("PR-AUC", f"{model_metrics.get('pr_auc', 0):.3f}")
    c3.metric("Failure Recall", f"{model_metrics.get('recall', 0):.2f}")
    c4.metric("Failure F1", f"{model_metrics.get('f1', 0):.2f}")


    st.markdown("### Selected Vehicle Model Signal")

    vehicle_failure_probability = float(latest["failure_probability"]) * 100
    vehicle_risk_score = float(latest["vehicle_risk_score"])
    vehicle_anomaly_score = float(latest["anomaly_score"])
    vehicle_risk_level = str(latest["risk_level"])
    vehicle_anomaly_flag = int(latest["anomaly_flag"])

    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "Failure Probability",
        f"{vehicle_failure_probability:.1f}%"
    )

    s2.metric(
        "Vehicle Risk Score",
        f"{vehicle_risk_score:.1f}/100"
    )

    s3.metric(
        "Anomaly Status",
        "Anomalous" if vehicle_anomaly_flag == 1 else "Normal"
    )

    s4.metric(
        "Risk Level",
        vehicle_risk_level
    )

    st.caption(
        f"Vehicle-specific model signal for {selected_vehicle}. "
        "Global ML metrics above evaluate the trained model; these indicators "
        "describe the selected vehicle's current analytical state."
    )

    st.caption(
        "Evaluation results from the current research prototype "
        "using synthetic automotive telemetry."
    )

    st.markdown("---")

    st.subheader("Predictive Maintenance Architecture")

    architecture = [
        "Automotive Telemetry",
        "Data Validation & Feature Engineering",
        "Failure Risk + Anomaly Detection",
        "Component Health Intelligence",
        "Vehicle Risk Engine",
        "Maintenance Prioritization",
        "Spare-Part Risk Signal",
    ]

    for i, step in enumerate(architecture):

        st.markdown(
            f"""
            <div style="
                border:1px solid #d9dee7;
                border-radius:8px;
                padding:10px;
                margin-bottom:8px;
                text-align:center;
                font-weight:600;
            ">
            {step}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if i < len(architecture) - 1:
            st.markdown(
                "<div style='text-align:center'>↓</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.subheader("Innovation Disclosure Concept")

    st.info(
        """
        **Predictive Spare-Part Intelligence**

        A prototype decision-support concept that combines:

        • failure probability  
        • sensor anomaly signals  
        • component health  
        • vehicle-level risk  
        • maintenance priority  

        The objective is to transform raw vehicle telemetry into a
        component-focused maintenance and spare-part prioritization signal.

        This is presented as an engineering innovation concept,
        not as a claimed patent or OEM-certified invention.
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("AI / Data Science Value")

        for item in [
            "Supervised failure-event classification",
            "Unsupervised anomaly detection",
            "Feature engineering",
            "Fleet-relative diagnostics",
            "Component health analytics",
            "Explainable maintenance signals",
        ]:
            st.markdown(f"- {item}")

    with col2:

        st.subheader("Automotive / Aftersales Value")

        for item in [
            "Vehicle health monitoring",
            "Component-level prioritization",
            "Predictive maintenance concept",
            "Service decision support",
            "Spare-part category prioritization",
            "Fleet risk management",
        ]:
            st.markdown(f"- {item}")

    st.markdown("---")

    st.subheader("Prototype Scope & Limitations")

    st.warning(
        """
        This project uses synthetic automotive telemetry and is intended
        as a research / portfolio prototype.

        Sensor-health scores, risk thresholds and spare-part mappings are
        analytical constructs. They are not OEM-certified recommendations,
        Mercedes-Benz production-data results, validated safety limits,
        or remaining-useful-life predictions.

        Automotive CAD/CAE/DFM and patent prior-art validation would require
        separate engineering workflows and domain evidence.
        """
    )


st.markdown("---")
st.caption(
    "Automotive Predictive Maintenance Intelligence | "
    "AI • ML • Anomaly Detection • Vehicle Health • Spare-Part Analytics"
)


st.markdown("""
<div class="auto-footer">
    PREMIUM AUTOMOTIVE INTELLIGENCE COCKPIT &nbsp;-&nbsp;
    AI / ML &nbsp;•&nbsp; PREDICTIVE MAINTENANCE &nbsp;•&nbsp;
    RESEARCH PROTOTYPE
</div>
""", unsafe_allow_html=True)
