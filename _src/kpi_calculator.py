def calculate_kpis(df):

    df_no_log = df[df["ActionID"] != "LOG"]

    total_actions = len(df_no_log)

    total_users = df["UPN"].count()

    unique_users = df["UPN"].nunique()

    return {
        "TotalActions": total_actions,
        "TotalUsers": total_users,
        "UniqueUsers": unique_users
    }