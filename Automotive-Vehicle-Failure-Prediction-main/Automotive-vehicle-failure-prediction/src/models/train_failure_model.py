import os
import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "synthetic_telemetry_data.csv",
)
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "failure_risk_model.joblib")

os.makedirs(MODEL_DIR, exist_ok=True)


# -----------------------------
# 1. Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Remove exact duplicate rows only.
df = df.drop_duplicates().copy()

# Parse timestamp.
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Target: observed failure event.
df["failure_target"] = (df["failure_type"] != "No Failure").astype(int)


# -----------------------------
# 2. Prevent target leakage
# -----------------------------
LEAKAGE_COLUMNS = [
    "failure_type",
    "failure_date",
    "failure_target",
    "engine_failure_imminent",
    "brake_issue_imminent",
    "battery_issue_imminent",
]

# Timestamp is retained only for audit/ordering, not as a model feature.
DROP_COLUMNS = LEAKAGE_COLUMNS + [
    "timestamp",
    "vehicle_id",
    "gps_latitude",
    "gps_longitude",
]

feature_columns = [
    c for c in df.columns
    if c not in DROP_COLUMNS
]

X = df[feature_columns].copy()
y = df["failure_target"].copy()


# -----------------------------
# 3. Feature groups
# -----------------------------
categorical_features = [
    c for c in ["brand"]
    if c in X.columns
]

numeric_features = [
    c for c in X.columns
    if c not in categorical_features
]


# -----------------------------
# 4. Preprocessing
# -----------------------------
numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
    ],
    remainder="drop",
)


# -----------------------------
# 5. Model
# -----------------------------
model = LogisticRegression(
    class_weight="balanced",
    max_iter=2000,
    random_state=42,
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# -----------------------------
# 6. Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42,
)

pipeline.fit(X_train, y_train)


# -----------------------------
# 7. Evaluation
# -----------------------------
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

print("=" * 60)
print("AUTOMOTIVE FAILURE-RISK MODEL")
print("=" * 60)
print(f"Rows used: {len(df)}")
print(f"Features used: {len(feature_columns)}")
print(f"Training rows: {len(X_train)}")
print(f"Test rows: {len(X_test)}")
print(f"Failure events: {y.sum()}")
print()

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()

print("Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)
pr_auc = average_precision_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1: {f1:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")
print(f"PR-AUC:  {pr_auc:.4f}")
print()

evaluation = {
    "model_type": "LogisticRegression",
    "random_state": 42,
    "dataset_rows": int(len(df)),
    "feature_count": int(len(feature_columns)),
    "training_rows": int(len(X_train)),
    "test_rows": int(len(X_test)),
    "failure_events": int(y.sum()),
    "metrics": {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
        "pr_auc": float(pr_auc),
    },
    "confusion_matrix": cm.tolist(),
    "target": "failure_target",
    "leakage_columns": LEAKAGE_COLUMNS,
}

EVALUATION_PATH = os.path.join(
    MODEL_DIR,
    "model_evaluation.json",
)

with open(EVALUATION_PATH, "w", encoding="utf-8") as f:
    json.dump(evaluation, f, indent=2)

print(f"Evaluation saved to: {EVALUATION_PATH}")
print()


# -----------------------------
# 8. Save model
# -----------------------------
artifact = {
    "pipeline": pipeline,
    "feature_columns": feature_columns,
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "target": "failure_target",
    "leakage_columns": LEAKAGE_COLUMNS,
    "model_type": "LogisticRegression",
    "dataset_rows": len(df),
    "failure_events": int(y.sum()),
}

joblib.dump(artifact, MODEL_PATH)

print(f"Model saved to: {MODEL_PATH}")
print("=" * 60)
