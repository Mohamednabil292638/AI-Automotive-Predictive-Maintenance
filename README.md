\# Automotive Predictive Maintenance \& Spare-Part Intelligence Platform



An end-to-end automotive AI research prototype combining vehicle telemetry analytics, failure-event classification, anomaly detection, component health scoring, vehicle risk prioritization, and spare-part maintenance intelligence.



Built with Python, SQL, Scikit-learn, Streamlit, Power BI, and synthetic automotive telemetry.



> \*\*Research Prototype:\*\* The dataset is synthetic and is not Mercedes-Benz/OEM data. The system demonstrates automotive AI, predictive-maintenance, anomaly-detection, and aftersales/spare-part analytics workflows.

---

## 🚀 Live Demo

### **[▶ Launch the Automotive Intelligence Command Center](https://automotive-predictive-maintenance.streamlit.app/)**

**Interactive Streamlit Demo**

Explore:

- 🚗 Fleet-level vehicle risk prioritization
- 🧠 Failure-event classification
- 🔎 Multivariate anomaly detection
- ❤️ Engine, brake & battery health scoring
- ⚡ Battery & electrical diagnostics
- 🔧 Maintenance recommendations
- 🧩 Spare-part prioritization
- 📊 Model performance and engineering KPIs

> **Demo:** The application is deployed as a public Streamlit research demonstration using synthetic automotive telemetry.

---

## ⭐ Project Highlights

| Capability | Implementation |
|---|---|
| Failure-event classification | Logistic Regression |
| Anomaly detection | Isolation Forest |
| Component health | Engine, Brake, Battery |
| Vehicle risk engine | Failure + anomaly + health signals |
| Spare-part intelligence | Generic component-to-part prioritization |
| Dashboard | Streamlit Automotive Intelligence Cockpit |
| Business analytics | Power BI |
| Dataset | 1,970 telemetry records / 50 vehicles |
| Failure events | 35 |
| Model ROC-AUC | **0.997** |
| Model PR-AUC | **0.920** |
| Failure Recall | **0.857** |
| Failure F1 | **0.857** |

---

## 🔗 Project Resources

- **Live Demo:** Automotive Predictive Maintenance Streamlit Application
- **Source Code:** GitHub Repository
- **Analytics:** Power BI Dashboard
- **Model Artifacts:** Scikit-learn + Joblib
- **Documentation:** Architecture, methodology, evaluation and limitations included below

---



\---



\## 🚗 Project Overview



This project demonstrates how automotive telemetry can be transformed into engineering-oriented intelligence for:



\- Vehicle failure-risk assessment

\- Sensor anomaly detection

\- Component health monitoring

\- Battery and electrical diagnostics

\- Maintenance prioritization

\- Spare-part risk prioritization

\- Fleet-level engineering analytics

\- Interactive vehicle intelligence



The Streamlit application provides an automotive intelligence cockpit where engineers can select individual vehicles, inspect sensor conditions, review model signals, and prioritize maintenance actions.



\---



\## 📊 Dataset



The project uses a synthetic automotive telemetry dataset containing:



| Metric | Value |

|---|---:|

| Vehicles | 50 |

| Telemetry records | 1,970 |

| Failure events | 35 |

| Failure classes | 9 |

| Data type | Synthetic research data |



Telemetry includes engine, braking, battery/electrical, vehicle dynamics, and environmental signals.



\### Example Signals



\- Engine temperature

\- Engine RPM

\- Oil pressure

\- Coolant temperature

\- Engine load

\- Air flow

\- Exhaust temperature

\- Vibration

\- Brake fluid level

\- Brake pad wear

\- Brake temperature

\- ABS signals

\- Wheel speeds

\- Battery voltage

\- Battery current

\- Battery temperature

\- Alternator output

\- Battery charge

\- Battery health

\- Vehicle speed

\- Ambient temperature



\---



\## 🧠 Machine Learning Pipeline



\### 1. Failure-Event Classification



A Logistic Regression classification pipeline is trained using:



\- StandardScaler

\- OneHotEncoder

\- Stratified train/test split

\- Class balancing

\- Leakage-aware feature selection



Failure-related leakage columns are excluded from the predictive feature set.



\### Model Evaluation



The current evaluated model uses:



\- Training records: 1,576

\- Test records: 394

\- Failure events: 35



| Metric | Result |

|---|---:|

| Accuracy | 0.995 |

| Precision | 0.857 |

| Recall | 0.857 |

| F1 Score | 0.857 |

| ROC-AUC | 0.997 |

| PR-AUC | 0.920 |



These metrics are stored in:



`models/model\_evaluation.json`



> These results represent a failure-event classification research prototype. They should not be interpreted as validated OEM production performance or as a guaranteed future-failure predictor.



\---



\## 🔎 2. Anomaly Detection



An Isolation Forest pipeline identifies unusual multivariate telemetry patterns.



The workflow performs:



1\. Sensor feature selection

2\. Median imputation

3\. Feature standardization

4\. Multivariate anomaly detection

5\. Anomaly scoring and flag generation



Output:



`data/vehicle\_anomaly\_scores.csv`



The current anomaly pipeline evaluates 1,970 telemetry records across 16 sensor/component features.



\---



\## ❤️ 3. Component Health Intelligence



The system calculates distribution-relative health scores for:



\- Engine

\- Brake

\- Battery



The results are stored in:



`data/vehicle\_component\_health.csv`



An overall vehicle health indicator supports downstream maintenance prioritization.



\---



\## ⚡ 4. Battery \& Electrical Intelligence



The application provides dedicated battery and electrical diagnostics using:



\- Battery voltage

\- Battery current

\- Alternator output

\- Battery charge

\- Battery health



The system distinguishes between:



\- Stable electrical condition

\- Electrical risk

\- Charging-system watch

\- Observed battery discharge



Negative battery current is interpreted as a discharge-direction signal rather than automatically being classified as a fault.



\---



\## 🎯 5. Vehicle Risk Prioritization



Vehicle-level intelligence combines:



\- Failure probability

\- Anomaly risk

\- Component health risk



\### Risk Formulation



```text

Vehicle Risk =

0.50 × Failure Probability

\+ 0.25 × Anomaly Risk

\+ 0.25 × Health Risk

```



The resulting score is mapped into:



\- Low

\- Moderate

\- High

\- Critical



Output:



`data/vehicle\_risk\_prioritization.csv`



This creates an engineering-oriented ranking for maintenance decision support.



\---



\## 🔧 6. Spare-Part Intelligence



The project extends vehicle risk analytics into generic aftersales and spare-part prioritization.



| Vehicle subsystem | Maintenance domain |

|---|---|

| Engine | Cooling, lubrication and thermal components |

| Brake | Pads, fluid and braking components |

| Battery | Battery, alternator and electrical charging components |



Priority levels:



\- \*\*P1\*\* — Immediate attention

\- \*\*P2\*\* — High priority

\- \*\*P3\*\* — Planned maintenance

\- \*\*P4\*\* — Monitor



Output:



`data/spare\_part\_risk\_prioritization.csv`



> This is generic component-to-part prioritization logic. It does not use OEM part numbers or claim compatibility with any specific manufacturer.



\---



\## 🖥️ 7. Interactive Automotive Intelligence Cockpit



The Streamlit application provides an engineering-focused interface for:



\- Fleet overview

\- Vehicle selection

\- Failure probability

\- Vehicle risk score

\- Anomaly status

\- Component health

\- Sensor diagnostics

\- Battery/electrical intelligence

\- Maintenance recommendations

\- Spare-part prioritization

\- Model evaluation metrics



\### Run Locally



From the project directory:



```powershell

streamlit run ".\\app\\streamlit\_app.py"

```



\---



\## 📈 8. Power BI Analytics



The repository also contains the Power BI dashboard used for executive and fleet analytics.



Dashboard areas include:



\- Executive fleet health overview

\- Failure analysis

\- Predictive maintenance and risk ranking



\### Executive Fleet Overview



!\[Executive Overview](Automotive-Vehicle-Failure-Prediction-main/Automotive-vehicle-failure-prediction/images/page1\_executive\_overview.png)



\### Failure Analysis



!\[Failure Analysis](Automotive-Vehicle-Failure-Prediction-main/Automotive-vehicle-failure-prediction/images/page2\_failure\_analysis.png)



\### Predictive Maintenance



!\[Predictive Maintenance](Automotive-Vehicle-Failure-Prediction-main/Automotive-vehicle-failure-prediction/images/page3\_predictive\_maintenance.png)



\---



\## 🏗️ Architecture



```text

Synthetic Automotive Telemetry

&#x20;           |

&#x20;           v

&#x20;    Data Preparation

&#x20;           |

&#x20;    +------+------+

&#x20;    |             |

&#x20;    v             v

Feature Engineering   EDA / SQL

&#x20;    |

&#x20;    v

+-----------------------+

| Machine Learning      |

|                       |

| Failure Classification|

| Anomaly Detection     |

+-----------------------+

&#x20;           |

&#x20;           v

&#x20;  Component Health

&#x20;           |

&#x20;           v

&#x20;  Vehicle Risk Engine

&#x20;           |

&#x20;           v

&#x20;  Spare-Part Risk Engine

&#x20;           |

&#x20;      +----+----+

&#x20;      |         |

&#x20;      v         v

&#x20; Streamlit   Power BI

&#x20;      |         |

&#x20;      +----+----+

&#x20;           |

&#x20;           v

&#x20;Engineering Intelligence

```



\---



\## 📁 Repository Structure



```text

Automotive-Vehicle-Failure-Prediction-main/

│

├── README.md

│

└── Automotive-Vehicle-Failure-Prediction-main/

&#x20;   │

&#x20;   └── Automotive-vehicle-failure-prediction/

&#x20;       │

&#x20;       ├── app/

&#x20;       │   └── streamlit\_app.py

&#x20;       │

&#x20;       ├── data/

&#x20;       │   ├── synthetic\_telemetry\_data.csv

&#x20;       │   ├── vehicle\_component\_health.csv

&#x20;       │   ├── vehicle\_anomaly\_scores.csv

&#x20;       │   ├── vehicle\_risk\_prioritization.csv

&#x20;       │   └── spare\_part\_risk\_prioritization.csv

&#x20;       │

&#x20;       ├── images/

&#x20;       │   ├── page1\_executive\_overview.png

&#x20;       │   ├── page2\_failure\_analysis.png

&#x20;       │   └── page3\_predictive\_maintenance.png

&#x20;       │

&#x20;       ├── models/

&#x20;       │   ├── failure\_risk\_model.joblib

&#x20;       │   ├── anomaly\_detector.joblib

&#x20;       │   └── model\_evaluation.json

&#x20;       │

&#x20;       ├── notebooks/

&#x20;       │   └── automotive\_vehicle\_failure\_prediction.ipynb

&#x20;       │

&#x20;       ├── powerbi/

&#x20;       │   └── automotive failure predication dashboard.pbix

&#x20;       │

&#x20;       ├── predications/

&#x20;       │   └── vehicle\_failure\_predictions.xls

&#x20;       │

&#x20;       ├── src/

&#x20;       │   ├── features/

&#x20;       │   │   └── component\_health.py

&#x20;       │   │

&#x20;       │   ├── models/

&#x20;       │   │   ├── train\_failure\_model.py

&#x20;       │   │   └── anomaly\_detector.py

&#x20;       │   │

&#x20;       │   ├── prediction/

&#x20;       │   │   └── vehicle\_risk\_engine.py

&#x20;       │   │

&#x20;       │   └── maintenance/

&#x20;       │       └── spare\_part\_risk.py

&#x20;       │

&#x20;       └── tests/

```



\---



\## 🛠️ Technology Stack



\### Programming \& Data



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- Joblib

\- SQL



\### Machine Learning



\- Logistic Regression

\- Isolation Forest

\- Feature engineering

\- Classification

\- Anomaly detection

\- Risk scoring

\- Model evaluation



\### Analytics \& Visualization



\- Streamlit

\- Power BI

\- Matplotlib

\- Seaborn

\- Excel



\### Engineering Concepts



\- Predictive maintenance

\- Automotive telemetry analytics

\- Component health monitoring

\- Failure-event analysis

\- Anomaly detection

\- Aftersales intelligence

\- Spare-part prioritization

\- Engineering KPI analysis



\---



\## 🔬 Engineering \& Innovation Perspective



The project demonstrates an automotive AI workflow:



```text

Vehicle Data

&#x20;    |

&#x20;    v

Signal Quality \& Feature Engineering

&#x20;    |

&#x20;    v

Failure / Anomaly Detection

&#x20;    |

&#x20;    v

Component Health Assessment

&#x20;    |

&#x20;    v

Vehicle Risk Prioritization

&#x20;    |

&#x20;    v

Maintenance Decision Support

&#x20;    |

&#x20;    v

Spare-Part Prioritization

```



The architecture can be extended with real-world:



\- Service records

\- Warranty claims

\- Vehicle diagnostics

\- Telematics

\- Parts-sales information

\- Validated engineering thresholds



when such data becomes available.



\---



\## ⚠️ Limitations



This project is intentionally presented as a research prototype.



\- The dataset is synthetic.

\- No Mercedes-Benz proprietary data is used.

\- Sensor thresholds are not OEM specifications.

\- The model has not been validated on production vehicle fleets.

\- Spare-part mappings are generic rather than OEM-specific.

\- The system does not claim actual patentability or a filed patent.

\- CAD/CAE/DFM workflows are outside the current implementation.

\- Production deployment would require additional validation, monitoring, calibration, and domain-engineering review.



\---



\## 🚀 Future Extensions



Potential engineering extensions include:



\- Real vehicle diagnostic datasets

\- Warranty-claim analytics

\- Service-history integration

\- Telematics time-series modeling

\- Temporal anomaly detection

\- Remaining Useful Life estimation

\- Component-level failure prediction

\- Explainable AI for engineering decisions

\- Parts-demand forecasting

\- Cost-aware maintenance optimization

\- CAD/CAE-assisted component analysis

\- Digital-twin integration

\- Engineering knowledge retrieval using GenAI

\- Automated engineering insight generation



\---



\## 👨‍💻 Author



\*\*Mohamed Nabil S\*\*



B.Tech — Artificial Intelligence \& Data Science



GitHub: https://github.com/Mohamednabil292638



LinkedIn: https://www.linkedin.com/in/mohamed-nabil-s-950104308/



\---



\## Project Information



\*\*Project:\*\* Automotive Predictive Maintenance \& Spare-Part Intelligence Platform



\*\*Domain:\*\* Automotive AI • Predictive Maintenance • Aftersales Analytics • Machine Learning



\*\*Project Type:\*\* Synthetic-data research and engineering prototype

```



After pasting the \*\*whole thing\*\*:



\*\*Ctrl + S → close Notepad.\*\*



Then tell me only:



\*\*“saved”\*\*



We will verify it before doing anything else.

