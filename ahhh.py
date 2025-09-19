import requests

url = "http://localhost:8000/api/sensor_data"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "api_key"
}
payload = {
    "temperature": 25.5,
    "pressure": 1013.25,
    "concentration": 0.85,
    "flow": 12.3
}

r = requests.post(url, json=payload, headers=headers)
print(r.status_code)
print(r.text)
