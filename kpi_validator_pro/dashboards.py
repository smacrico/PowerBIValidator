import streamlit as st
import pandas as pd

st.title("Power BI KPI Validation")

results = validate(python_kpis, powerbi_kpis)

df = pd.DataFrame(results)

st.dataframe(df)

mismatch = df[df["Match"] == False]

if len(mismatch) == 0:
    st.success("All KPIs match Power BI")
else:
    st.error("Some KPIs do not match")
    st.dataframe(mismatch)