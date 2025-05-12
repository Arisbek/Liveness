import os
from dotenv import load_dotenv

import requests

# Load environment variables from .env file
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")

def test_log():
    login_response = requests.post(f"{SERVER_URL}/api/auth/login", json={"owner": "admin", "password": "master"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{SERVER_URL}/api/generate_instructions", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["turn right", "turn left", "turn up", "turn down"]