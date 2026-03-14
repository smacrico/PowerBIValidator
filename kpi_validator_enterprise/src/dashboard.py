import streamlit as st
import pandas as pd

st.title("Power BI Model Test Results")

results = pd.read_csv("test_results.csv")

st.dataframe(results)