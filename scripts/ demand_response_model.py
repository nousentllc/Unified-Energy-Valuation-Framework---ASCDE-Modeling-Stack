
import pandas as pd

def model_demand_response(path):
    print(f"🔍 Modeling demand response from: {path}")
    df = pd.read_excel(path)
    
    if "ProgramType" in df.columns:
        print("📊 Program types:\n", df["ProgramType"].value_counts(dropna=False))
    else:
        print("⚠️ 'ProgramType' column missing")

    # Reliability alignment
    try:
        df["DispatchStart"] = pd.to_datetime(df["DispatchStart"])
        df["DispatchEnd"] = pd.to_datetime(df["DispatchEnd"])
        df["IsPeakAligned"] = df["DispatchStart"].dt.hour.between(17, 21)
        df["ELCC_Proxy"] = df["IsPeakAligned"].astype(int) * df.get("ResponseCapacity_kW", 1)
        print("✅ ELCC proxy scores:\n", df["ELCC_Proxy"].describe())
    except Exception as e:
        print("⚠️ Dispatch time columns missing or unparseable:", e)

if __name__ == "__main__":
    model_demand_response("data/Demand_Response_2023.xlsx")
