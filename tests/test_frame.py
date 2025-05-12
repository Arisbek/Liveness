# test_script.py
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")

def test_upload_file():
    # Step 1: Log in to get the token
    login_response = requests.post(f"{SERVER_URL}/api/auth/login", json={"owner": "admin", "password": "master"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    file_path = "tests/person_2.jpg"
    assert os.path.exists(file_path), f"File not found: {file_path}"

    # Step 2: Use the TestClient to upload the file
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(f"{SERVER_URL}/api/check/frame", headers=headers, files=files)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["result"] == "valid"

if __name__ == "__main__":
    import pytest
    pytest.main()