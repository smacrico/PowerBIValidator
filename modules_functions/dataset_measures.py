
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

measures = measures[["MEASURE_NAME", "EXPRESSION"]]

print(measures)

def run_measure(conn, measure_name):

    dax = f"""
    EVALUATE
    ROW(
        "Result", [{measure_name}]
    )
    """

    with conn.cursor().execute(dax) as cur:
        result = cur.fetchone()[0]

    return result


measure_results = {}

with Pyadomd(connection_string) as conn:

    for m in measures["MEASURE_NAME"]:

        try:
            value = run_measure(conn, m)
            measure_results[m] = value

        except Exception as e:
            measure_results[m] = "ERROR"


            




def get_measures(dataset_id):

    token = get_access_token()

    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(url, headers=headers)

    return r.json()def execute_dax(dataset_id, dax_query):

    token = get_access_token()

    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "queries": [
            {"query": dax_query}
        ],
        "serializerSettings": {
            "includeNulls": True
        }
    }

    r = requests.post(url, headers=headers, json=body)

    return r.json()