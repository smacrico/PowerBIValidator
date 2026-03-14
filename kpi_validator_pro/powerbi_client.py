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

def get_measures(dataset_id):

    token = get_access_token()

    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(url, headers=headers)

    return r.json()

def execute_dax(dataset_id, dax_query):

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
