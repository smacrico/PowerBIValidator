import pandas as pd

def actions_per_user(df):

    return (
        df.groupby("UserUPN")
        .size()
        .reset_index(name="PythonActions")
    )


def compare_user_actions(df, pbi_df):

    python_counts = actions_per_user(df)

    merged = python_counts.merge(
        pbi_df,
        on="UserUPN",
        how="outer"
    )

    merged["PowerBIActions"] = merged["PowerBIActions"].fillna(0)
    merged["PythonActions"] = merged["PythonActions"].fillna(0)

    merged["Difference"] = merged["PythonActions"] - merged["PowerBIActions"]

    return merged.sort_values("Difference", ascending=False)
