import pandas as pd


def reconcile_datasets(python_df, powerbi_df):

    python_df["source"] = "Python"
    powerbi_df["source"] = "PowerBI"

    combined = pd.concat([python_df, powerbi_df])

    duplicates = combined.duplicated(
        subset=["ActionID", "UserUPN", "DateSubmited"],
        keep=False
    )

    mismatches = combined[~duplicates]

    return mismatches
