import httpx

API_BASE_URL = "https://localhost:8000/api"

def api_get(endpoint: str, params=None):
    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            response = client.get(url, params=params)
            return response.json()
    except Exception as e:
        return {
            "response_status": False,
            "status_code": 500,
            "message": f"GET request failed: {e}",
            "source_output": None
        }

def api_post(endpoint: str, payload=None):
    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            response = client.post(url, json=payload)
            return response.json()
    except Exception as e:
        return {
            "response_status": False,
            "status_code": 500,
            "message": f"POST request failed: {e}",
            "source_output": None
        }
