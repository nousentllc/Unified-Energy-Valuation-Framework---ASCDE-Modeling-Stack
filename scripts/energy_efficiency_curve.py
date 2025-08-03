
import pandas as pd
import matplotlib.pyplot as plt

def build_efficiency_curve(path):
    print(f"🔍 Building efficiency curves from: {path}")
    df = pd.read_excel(path)
    
    if "MeasureType" in df.columns:
        print("📊 Measure categories:\n", df["MeasureType"].value_counts(dropna=False))
    
    if {"Participants", "SavingsPerUnit_kWh"}.issubset(df.columns):
        df["AnnualSavings_kWh"] = df["Participants"] * df["SavingsPerUnit_kWh"]
        savings_by_type = df.groupby("MeasureType")["AnnualSavings_kWh"].sum().sort_values(ascending=False)
        print("🏆 Top Measures:\n", savings_by_type.head(5))

        savings_by_type.plot(kind='barh')
        plt.title("Annual kWh Savings by Measure Type")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    build_efficiency_curve("data/Energy_Efficiency_2023.xlsx")
