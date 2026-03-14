import sqlite3
import pandas as pd
from config import DB_PATH

def read_actions():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT ActionID, UPN, ActionDate
    FROM UserActions
    """

    df = pd.read_sql(query, conn)

    df["ActionDate"] = pd.to_datetime(df["ActionDate"])

    return df