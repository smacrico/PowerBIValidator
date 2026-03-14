import requests
import pandas as pd

def execute_dax(dataset_id, dax_query, token):

    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "queries": [
            {"query": dax_query}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    result = response.json()

    rows = result["results"][0]["tables"][0]["rows"]

    return pd.DataFrame(rows)
