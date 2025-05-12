import os
from dotenv import load_dotenv

import requests

# Load environment variables from .env file
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")


def test_log():
    login_response = requests.post(f"{SERVER_URL}/api/auth/login", json={"owner": "admin", "password": "master"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    body = {
        "owner": "admin",
        "old_password": "master",
        "new_password": "mas"
    }
    
    response = requests.post(f"{SERVER_URL}/api/auth/reset-password", headers=headers, json=body)
    assert response.status_code == 200
    # assert response.json() == {"owner"}
    login_response = requests.post(f"{SERVER_URL}/api/auth/login", json={"owner": "admin", "password": "mas"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    body2 = {
        "owner": "admin",
        "old_password": "mas",
        "new_password": "master"
    }
    
    response = requests.post(f"{SERVER_URL}/api/auth/reset-password", headers=headers, json=body2)
    assert response.status_code == 200