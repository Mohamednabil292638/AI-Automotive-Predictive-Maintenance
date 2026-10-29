
# 🚗 Automotive Predictive Maintenance & Vehicle Health Analytics

An end-to-end data science solution that detects early failure signals in automotive telemetry, helping fleet managers transition from reactive repairs to data-driven predictive maintenance.

---

## 📈 Executive Summary & Key Results

By analyzing vehicle sensor data and training a machine learning classification pipeline, this project successfully predicts vehicle failure risks with high reliability:

* **100% Failure Detection (Recall = 1.00):** Identified all 7 actual vehicle failures in the test dataset ($N=394$).
* **Near-Zero False Alarms (Precision = 0.88):** Produced only 1 false positive out of 387 normal vehicle observations.
* **Top Performance Metrics:** Achieved an **ROC-AUC of 0.9989** and a **PR-AUC of 0.9379**.
* **Primary Risk Drivers:** Electrical degradation (Battery Voltage & Current) and Thermal/Hydraulic load (Brake Fluid Level & Brake Temperature) are the strongest statistical predictors of impending failure.

---

## 📊 Interactive Dashboard Insights

The accompanying 3-page Power BI dashboard converts analytical findings into actionable fleet management screens:

### 1. Executive Fleet Health Overview
Monitors total fleet population, operational hours, and key failure indicators at a glance.
![Executive Overview](Automotive-vehicle-failure-prediction/images/page1_executive_overview.png)

### 2. Failure Pattern & Sensor Diagnostics
Explores root causes, comparing electrical, brake, and engine telemetry across vehicle brands.
![Failure Analysis](Automotive-vehicle-failure-prediction/images/page2_failure_analysis.png)

### 3. Predictive Risk Ranking & Maintenance Action
Ranks vehicles by ML-predicted failure probability to help engineering teams prioritize diagnostic inspections.
![Predictive Maintenance](Automotive-vehicle-failure-prediction/images/page3_predictive_maintenance.png)

---

## 💡 Business Impact & Engineering Recommendations

1. **Prioritize Electrical & Brake Subsystems:** Battery health (voltage/current) and brake fluid levels showed the strongest correlation with failure risk. Real-time alerts should be configured for voltage drops and fluid loss.
2. **Shift to Probability-Based Maintenance:** Maintenance teams should prioritize vehicles scoring in the top risk probability tier rather than relying solely on fixed mileage schedules.
3. **Early Warning via Vibration Monitoring:** Elevated mechanical vibration and engine temperature serve as secondary signals for physical component wear.

---

## 🛠️ Tech Stack & Workflow

* **Analytics & Querying:** SQL (MySQL / DuckDB) for relational data aggregations and health metric extraction.
* **Data Processing & ML:** Python (Pandas, NumPy, Scikit-Learn) for EDA, feature engineering, and Logistic Regression modeling.
* **Business Intelligence:** Power BI (DAX) for interactive executive reporting and risk visualization.

---

## 📁 Repository Structure

```text
automotive-vehicle-failure-prediction/
│
├── notebooks/      └── automotive_vehicle_failure_prediction.ipynb
├── sql/            └── vehicle_failure_analysis.sql
├── predictions/    └── vehicle_failure_predictions.csv
├── powerbi/        └── automotive_predictive_maintenance.pbix
├── images/         ├── page1_executive_overview.png
│                   ├── page2_failure_analysis.png
│                   └── page3_predictive_maintenance.png
└── README.md
