import sqlite3
import pandas as pd

def read_actions(db_path):

    conn = sqlite3.connect(db_path)

    query = """
    SELECT ActionID, UPN, ActionDate
    FROM UserActions
    """

    df = pd.read_sql(query, conn)

    df["ActionDate"] = pd.to_datetime(df["ActionDate"])

    return df