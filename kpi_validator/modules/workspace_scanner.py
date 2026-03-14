import requests

def get_workspaces(token):

    url = "https://api.powerbi.com/v1.0/myorg/groups"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    return response.json()["value"]


def get_datasets(workspace_id, token):

    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    return response.json()["value"]

def get_reports(workspace_id, token):

    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    return response.json()["value"]

