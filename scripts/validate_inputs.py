import pandas as pd
import os
import json

def validate_queue_data(path):
    print(f"🔍 Validating queue data at: {path}")
    try:
        df = pd.read_excel(path)
        required_cols = ["QueueDate", "CODDate", "Status"]
        for col in required_cols:
            if col not in df.columns:
                print(f"❌ Missing column: {col}")
        df["QueueDate"] = pd.to_datetime(df["QueueDate"], errors="coerce")
        df["CODDate"] = pd.to_datetime(df["CODDate"], errors="coerce")
        print("📊 Status breakdown:\n", df["Status"].value_counts(dropna=False))
    except Exception as e:
        print(f"❌ Queue validation failed: {e}")

def validate_elcc_timeseries(resource_path, netload_path):
    print(f"🔍 Validating ELCC time series...")
    try:
        res = pd.read_csv(resource_path, parse_dates=["Timestamp"])
        net = pd.read_excel(netload_path, parse_dates=["Timestamp"])
        print(f"✅ Resource range: {res['Timestamp'].min()} → {res['Timestamp'].max()}")
        print(f"✅ Net load range: {net['Timestamp'].min()} → {net['Timestamp'].max()}")
    except Exception as e:
        print(f"❌ Time series validation failed: {e}")

def validate_penetration_json(path):
    print(f"🔍 Validating penetration ratios JSON...")
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        print("✅ Penetration tech types:", list(data.keys())[:5])
    except Exception as e:
        print(f"❌ Penetration JSON error: {e}")

def validate_eue_csv(path):
    print(f"🔍 Validating EUE CSV...")
    try:
        df = pd.read_csv(path)
        print("✅ EUE sample:\n", df.head(2))
    except Exception as e:
        print(f"❌ EUE CSV error: {e}")

def validate_config_json(path):
    print(f"🔍 Validating modeling config...")
    try:
        with open(path, 'r') as f:
            cfg = json.load(f)
        print("✅ Config keys:", list(cfg.keys()))
    except Exception as e:
        print(f"❌ Config JSON error: {e}")

if __name__ == "__main__":
    validate_queue_data("data/July Queue's 2025.xlsx")
    validate_elcc_timeseries("data/20250728_rt_lmp_final.csv", "data/EIA_930A_2023_with layout.xlsx")
    validate_penetration_json("data/penetration_ratios.json")
    validate_eue_csv("data/UEVF-IQ - Foundational.csv")
    validate_config_json("data/modeling_config.json")