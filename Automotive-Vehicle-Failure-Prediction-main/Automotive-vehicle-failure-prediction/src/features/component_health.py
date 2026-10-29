import pandas as pd
import numpy as np


def min_max_risk(series):
    series = pd.to_numeric(series, errors="coerce")
    low = series.quantile(0.05)
    high = series.quantile(0.95)

    if pd.isna(low) or pd.isna(high) or high <= low:
        return pd.Series(0.0, index=series.index)

    risk = (series - low) / (high - low)
    return risk.clip(0, 1)


def calculate_component_health(df):
    result = df.copy()

    engine_signals = [
        "engine_temp_c",
        "oil_pressure_psi",
        "coolant_temp_c",
        "engine_load_percent",
        "exhaust_gas_temp_c",
        "vibration_level",
    ]

    brake_signals = [
        "brake_fluid_level_psi",
        "brake_pad_wear_mm",
        "brake_temp_c",
        "abs_fault_indicator",
    ]

    battery_signals = [
        "battery_voltage_v",
        "battery_current_a",
        "battery_temp_c",
        "alternator_output_v",
        "battery_charge_percent",
        "battery_health_percent",
    ]

    def subsystem_risk(columns):
        available = [c for c in columns if c in result.columns]

        if not available:
            return pd.Series(0.0, index=result.index)

        risks = []

        for column in available:
            values = pd.to_numeric(result[column], errors="coerce")

            # For health/level/voltage signals, lower values can indicate degradation.
            if column in {
                "oil_pressure_psi",
                "coolant_temp_c",
                "brake_fluid_level_psi",
                "battery_voltage_v",
                "alternator_output_v",
                "battery_charge_percent",
                "battery_health_percent",
            }:
                risk = 1 - min_max_risk(values)
            else:
                risk = min_max_risk(values)

            risks.append(risk)

        return pd.concat(risks, axis=1).mean(axis=1).fillna(0)

    result["engine_risk"] = subsystem_risk(engine_signals)
    result["brake_risk"] = subsystem_risk(brake_signals)
    result["battery_risk"] = subsystem_risk(battery_signals)

    result["overall_component_risk"] = result[
        ["engine_risk", "brake_risk", "battery_risk"]
    ].mean(axis=1)

    result["engine_health_score"] = ((1 - result["engine_risk"]) * 100).round(1)
    result["brake_health_score"] = ((1 - result["brake_risk"]) * 100).round(1)
    result["battery_health_score"] = ((1 - result["battery_risk"]) * 100).round(1)
    result["overall_health_score"] = (
        (1 - result["overall_component_risk"]) * 100
    ).round(1)

    return result


if __name__ == "__main__":
    print("Component health module ready.")
