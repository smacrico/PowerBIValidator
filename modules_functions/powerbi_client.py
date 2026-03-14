import requests
import msal


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]

def get_access_token():

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    token = app.acquire_token_for_client(scopes=SCOPE)

    return token["access_token"]



# Connect to Power BI Model from Python
from pyadomd import Pyadomd
import pandas as pd

connection_string = """
Provider=MSOLAP;
Data Source=powerbi://api.powerbi.com/v1.0/myorg/WorkspaceName;
Initial Catalog=DatasetName;
"""

with Pyadomd(connection_string) as conn:

    query = "SELECT * FROM $SYSTEM.MDSCHEMA_MEASURES"

    with conn.cursor().execute(query) as cur:
        measures = pd.DataFrame(cur.fetchall(), columns=[c.name for c in cur.description])

print(measures.head())
