
import pandas as pd

import sqlite3

conn = sqlite3.connect("actions.db")

df = pd.read_sql("SELECT * FROM UserActions", conn)

df_no_log = df[df["ActionID"] != "LOG"]

python_kpis = {     
    "Total Actions": len(df_no_log),
    "Unique Users": df["UPN"].nunique(),
    "Total Users": df["UPN"].count()
}

validation = []

for kpi in python_kpis:

    validation.append({
        "Metric": kpi,
        "Python": python_kpis[kpi],
        "PowerBI": measure_results.get(kpi),
        "Match": python_kpis[kpi] == measure_results.get(kpi)
    })

validation_df = pd.DataFrame(validation)

def validate(python_kpis, powerbi_kpis):

    results = []

    for kpi in python_kpis.keys():

        results.append({
            "Metric": kpi,
            "Python": python_kpis[kpi],
            "PowerBI": powerbi_kpis[kpi],
            "Match": python_kpis[kpi] == powerbi_kpis[kpi]
        })

    return results