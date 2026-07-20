# nessus_api/auth.py

ACCESS_KEY = " "
SECRET_KEY = " "

NESSUS_URL = "https://localhost:8834"

HEADERS = {
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}",
    "Content-Type": "application/json"
}
