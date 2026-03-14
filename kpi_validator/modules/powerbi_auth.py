from msal import ConfidentialClientApplication

TENANT_ID = "YOUR_TENANT"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_SECRET"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]

def get_access_token():

    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    token = app.acquire_token_for_client(scopes=SCOPE)

    return token["access_token"]
