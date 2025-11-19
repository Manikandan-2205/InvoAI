import httpx
import os
from utils.result import Result

api_base_url = os.getenv("API_BASE_URL")

def get_vendor_list():
    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            response = client.get(f"{api_base_url}/v1/vendor/get-all-vendors")
            response.raise_for_status()
            return Result.Ok(data=response.json())
    except httpx.HTTPStatusError as e:
        return Result.Fail(message=f"HTTP error: {e.response.status_code} - {e.response.text}", code=e.response.status_code)
    except Exception as e:
        return Result.Fail(message=str(e))
    

def add_vendor(vendor_name, created_by=30026427):
    url = f"{api_base_url}/v1/vendor/create-new-vendor"

    payload = {
        "vendor_name": vendor_name,
        "is_deleted": 0,
        "created_by": created_by
    }

    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return Result.Ok(data=response.json())
    except httpx.HTTPStatusError as e:
        return Result.Fail(message=f"HTTP error: {e.response.status_code} - {e.response.text}", code=e.response.status_code)
    except Exception as e:
        return Result.Fail(message=str(e))
    
def get_vendor_by_id(id):
    url = f"{api_base_url}/v1/vendor/get-vendor-by-id/{id}"
    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return Result.Ok(data=response.json())
    except httpx.HTTPStatusError as e:
        return Result.Fail(message=f"HTTP error: {e.response.status_code} - {e.response.text}", code=e.response.status_code)
    except Exception as e:
        return Result.Fail(message=str(e))
        