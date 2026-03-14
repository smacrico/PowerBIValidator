import sqlite3
import pandas as pd
import streamlit as st

# -----------------------------
# Database connection
# -----------------------------
DB_PATH = "C:\smakrykoDev\GitHub_dls\PowerBIValidator\data\Actions.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT ActionID, UPN, ActionDate
FROM UserActions
"""

df = pd.read_sql(query, conn)
df["ActionDate"] = pd.to_datetime(df["ActionDate"])

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Power BI KPI Validator")

st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", df["ActionDate"].min())
end_date = st.sidebar.date_input("End Date", df["ActionDate"].max())

# Filter dataset
filtered = df[
    (df["ActionDate"] >= pd.to_datetime(start_date)) &
    (df["ActionDate"] <= pd.to_datetime(end_date))
]

# -----------------------------
# KPI calculations
# -----------------------------

# Exclude LOG actions
filtered_no_log = filtered[filtered["ActionID"] != "LOG"]

total_actions = len(filtered_no_log)

total_users = filtered["UPN"].count()

unique_users = filtered["UPN"].nunique()

# -----------------------------
# NEW KPI calculations
# -----------------------------

# Actions per user
actions_per_user = (
    total_actions / unique_users if unique_users > 0 else 0
)

# Daily Active Users
dau = (
    filtered.groupby(filtered["ActionDate"].dt.date)["UPN"]
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

    # -----------------------------
# Daily Active Users
# -----------------------------
st.subheader("Daily Active Users")

st.line_chart(
    dau.set_index("ActionDate")["DailyActiveUsers"]
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