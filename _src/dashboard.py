# streamlit run src/dashboard.py

import streamlit as st
from db_reader import read_actions
from kpi_calculator import calculate_kpis
import pandas as pd

df = read_actions()

kpis = calculate_kpis(df)

st.title("KPI Validator")

col1, col2, col3 = st.columns(3)

col1.metric("Total Actions", kpis["TotalActions"])
col2.metric("Total Users", kpis["TotalUsers"])
col3.metric("Unique Users", kpis["UniqueUsers"])

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


st.title("Power BI Measure Validator")

st.dataframe(validation_df)

if validation_df["Match"].all():
    st.success("All measures match")
else:
    st.error("Some measures do not match Power BI")
    