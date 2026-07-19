# nessus_api/auth.py

ACCESS_KEY = "649b5e0c984c1cafcfb2a3e851db9920f630f3d5f4840361b5c46bcbe04a0d8c"
SECRET_KEY = "4b83aeb16bef255059a5cd47e62195276b89a1024579777db0111e62b9a49d19"

NESSUS_URL = "https://localhost:11127"

HEADERS = {
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}",
    "Content-Type": "application/json"
}