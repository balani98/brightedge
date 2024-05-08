import requests
from requests.auth import HTTPBasicAuth



def auth_with_BE():
    # Headers with Basic Authentication
    headers = {
        "Content-Type": "text/plain",
        "Accept": "application/json",
    }
    return headers
