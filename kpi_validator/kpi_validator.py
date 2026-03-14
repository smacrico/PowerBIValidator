import sqlite3
import pandas as pd
import streamlit as st

# -----------------------------
# Database connection
# -----------------------------
DB_PATH = "C:\smakrykoDev\GitHub_dls\PowerBIValidator\data\Actions.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT ActionID, UserUPN, DateSubmited
FROM M365Analytics
"""

df = pd.read_sql(query, conn)
df["DateSubmited"] = pd.to_datetime(df["DateSubmited"])

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Power BI KPI Validator")

st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", df["DateSubmited"].min())
end_date = st.sidebar.date_input("End Date", df["DateSubmited"].max())

# Filter dataset
filtered = df[
    (df["DateSubmited"] >= pd.to_datetime(start_date)) &
    (df["DateSubmited"] <= pd.to_datetime(end_date))
]

# -----------------------------
# KPI calculations
# -----------------------------

# Exclude LOG actions
filtered_no_log = filtered[filtered["ActionID"] != "LOG"]

total_actions = len(filtered_no_log)

total_users = filtered["UserUPN"].count()

unique_users = filtered["UserUPN"].nunique()

# -----------------------------
# NEW KPI calculations
# -----------------------------

# Actions per user
actions_per_user = (
    total_actions / unique_users if unique_users > 0 else 0
)

# Daily Active Users
dau = (
    filtered.groupby(filtered["DateSubmited"].dt.date)["UserUPN"]
    .nunique()
    .reset_index(name="DailyActiveUsers")
)

# Action Type Breakdown
action_breakdown = (
    filtered["ActionID"]
    .value_counts()
    .reset_index()
)

action_breakdown.columns = ["ActionID", "Count"]

# -----------------------------
# Display KPIs
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Actions (excl LOG)", total_actions)
col2.metric("Total Users", total_users)
col3.metric("Unique Users", unique_users)
col4.metric("Actions per User", round(actions_per_user, 2))

# -----------------------------
# Power BI KPI Input
# -----------------------------
st.sidebar.header("Power BI KPI Values")

pbi_actions = st.sidebar.number_input("Power BI Total Actions")
pbi_users = st.sidebar.number_input("Power BI Total Users")
pbi_unique = st.sidebar.number_input("Power BI Unique Users")
pbi_actions_per_user = st.sidebar.number_input("Power BI Actions per User")

# -----------------------------
# Comparison
# -----------------------------
comparison = pd.DataFrame({
    "Metric": [
        "Total Actions",
        "Total Users",
        "Unique Users",
        "Actions per User"
    ],
    "Python Result": [
        total_actions,
        total_users,
        unique_users,
        round(actions_per_user, 2)
    ],
    "Power BI Result": [
        pbi_actions,
        pbi_users,
        pbi_unique,
        pbi_actions_per_user
    ]
})

comparison["Match"] = comparison["Python Result"] == comparison["Power BI Result"]

st.subheader("Validation Results")
st.dataframe(comparison)

if comparison["Match"].all():
    st.success("All measures match Power BI")
else:
    st.error("Some measures do not match Power BI")

st.subheader("User Drilldown Validation")

if st.checkbox("Enable user drilldown"):

    uploaded = st.file_uploader(
        "Upload Power BI user export (CSV)"
    )

    if uploaded:

        pbi_user_df = pd.read_csv(uploaded)

        from modules.drilldown_validator import compare_user_actions

        drilldown = compare_user_actions(filtered, pbi_user_df)

        st.dataframe(drilldown)


# -----------------------------
 # Power BI vs Python KPI Diff Analyzer
# -----------------------------
python_kpis = {
    "TotalActions": total_actions,
    "TotalUsers": total_users,
    "UniqueUsers": unique_users
}

powerbi_kpis = {
    "TotalActions": pbi_actions,
    "TotalUsers": pbi_users,
    "UniqueUsers": pbi_unique
}

from modules.diff_analyzer import analyze_kpi_differences

diff = analyze_kpi_differences(python_kpis, powerbi_kpis)

st.dataframe(diff)




    
# -----------------------------
# Daily Active Users
# -----------------------------
st.subheader("Daily Active Users")

st.line_chart(
    dau.set_index("DateSubmited")["DailyActiveUsers"]
)

st.dataframe(dau)

# -----------------------------
# Action Type Breakdown
# -----------------------------
st.subheader("Action Type Breakdown")

st.bar_chart(
    action_breakdown.set_index("ActionID")
)

st.dataframe(action_breakdown)



# -----------------------------
# Raw data preview
# -----------------------------
st.subheader("Filtered Data")
st.dataframe(filtered)


# -----------------------------
# DAX to Python Translator"
# -----------------------------

st.subheader("DAX to Python Translator")

dax_input = st.text_area("Paste DAX measure")

if dax_input:

    from modules.dax_translator import translate_dax

    python_equivalent = translate_dax(dax_input)

    st.code(python_equivalent)


# -----------------------------
# Dataset Reconciliation Report
# -----------------------------   
st.subheader("Dataset Reconciliation")

uploaded_dataset = st.file_uploader(
    "Upload Power BI dataset export"
)

if uploaded_dataset:

    pbi_df = pd.read_csv(uploaded_dataset)

    from modules.reconciliation_report import reconcile_datasets

    mismatches = reconcile_datasets(filtered, pbi_df)

    st.write("Mismatched rows")

    st.dataframe(mismatches)
