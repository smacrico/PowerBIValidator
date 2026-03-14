import pandas as pd


def analyze_kpi_differences(python_kpis, powerbi_kpis):

    df = pd.DataFrame({
        "Metric": python_kpis.keys(),
        "Python": python_kpis.values(),
        "PowerBI": powerbi_kpis.values()
    })

    df["Difference"] = df["Python"] - df["PowerBI"]

    df["Match"] = df["Difference"] == 0

    return df
