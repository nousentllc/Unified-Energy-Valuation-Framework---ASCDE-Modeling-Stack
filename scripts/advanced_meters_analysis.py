import pandas as pd
import argparse

def analyze_advanced_meters(path, output_path):
    print(f"🔍 Analyzing advanced meters from: {path}")
    df = pd.read_excel(path)

    # Rename for uniformity
    if "Utility Name" in df.columns:
        df.rename(columns={"Utility Name": "Utility"}, inplace=True)

    def safe_filter(df, keyword1, keyword2):
        filtered = df.filter(like=keyword1).filter(like=keyword2)
        if filtered.shape[1] == 0:
            raise KeyError(f"No columns match: '{keyword1}' and '{keyword2}'")
        return filtered.iloc[:, 0]

    try:
        df["AMI_Total"] = safe_filter(df, "Number AMI-", "Total")
        df["Meter_Total"] = safe_filter(df, "Total Numbers of Meters", "Total")
        df["PenetrationRate"] = df["AMI_Total"] / df["Meter_Total"]

        df["AMR_Total"] = safe_filter(df, "Number AMR-", "Total")
        df["Std_Total"] = safe_filter(df, "Standard (non AMR/AMI)", "Total")
        df["AMI_Energy"] = safe_filter(df, "Energy Served - AMI", "Total")
        df["DigitalAccess"] = safe_filter(df, "Daily Digital Access", "Total")
        df["DLC_Customers"] = safe_filter(df, "Direct Load Control", "Total")

        grouped = df.groupby("Utility")["PenetrationRate"].mean().sort_values(ascending=False)
        print("📈 AMI Penetration by Utility:\n", grouped.head(10))

        if "State" in df.columns:
            regional = df.groupby("State")["PenetrationRate"].mean().sort_values(ascending=False)
            print("\n📍 Average AMI Penetration by State:")
            print(regional.head(10))

        print("\n🔌 Direct Load Control Customers (Top 5):")
        print(df[["Utility", "DLC_Customers"]].dropna().sort_values("DLC_Customers", ascending=False).head(5))

        print("\n🌐 Customers with Digital Access (Top 5):")
        print(df[["Utility", "DigitalAccess"]].dropna().sort_values("DigitalAccess", ascending=False).head(5))

        # Export output
        df.sort_values("PenetrationRate", ascending=False).to_csv(output_path, index=False)
        print(f"\n📁 Output saved to: {output_path}")

    except Exception as e:
        print(f"❌ Failed to calculate metering metrics: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Advanced Meter Deployment Data")
    parser.add_argument("--input", default="data/Advanced_Meters_2023.xlsx", help="Path to input Excel file")
    parser.add_argument("--output", default="outputs/advanced_meter_summary.csv", help="Path to save output CSV")
    args = parser.parse_args()

    analyze_advanced_meters(args.input, args.output)