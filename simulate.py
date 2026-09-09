import requests
from datetime import datetime

WEBHOOK_URL = "http://localhost:8000/webhook"

event = {
    "event_type": "motion",
    "device_id": "cam_back_door",
    "device_name": "Back Door",
    "timestamp": "2026-09-09T02:14:00Z",
    "request_id": "test-001"
}

response = requests.post(WEBHOOK_URL, json=event)
print(response.status_code, response.json())
