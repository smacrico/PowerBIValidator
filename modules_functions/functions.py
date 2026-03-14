def calculate_kpis(df):
    no_log = df[df["ActionID"] != "LOG"]

    return {
        "total_actions": len(no_log),
        "total_users": df["UPN"].count(),
        "unique_users": df["UPN"].nunique()
    }