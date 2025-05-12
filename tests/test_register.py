
import os
from dotenv import load_dotenv
import psycopg2

import requests

# Load environment variables from .env file
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")


db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')



def test_log():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()
    login_response = requests.post(f"{SERVER_URL}/api/auth/login", json={"owner": "admin", "password": "master"})
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    body = {
        "owner": "Mock",
        "password": "123"
    }
    response = requests.post(f"{SERVER_URL}/api/auth/register", headers=headers, json=body)
    assert response.status_code == 200
    u = response.json()
    assert u["owner"] == "Mock"
    assert u["message"] == "Registration successful"

    cur.execute("DELETE FROM services WHERE owner='Mock';")
    # Commit the transaction
    conn.commit()

    cur.close()
    conn.close()