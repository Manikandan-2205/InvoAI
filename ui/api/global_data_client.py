import httpx
import os
from utils.result import Result

api_base_url = os.getenv("API_BASE_URL")



def get_vendor_list():
    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            response = client.get(f"{api_base_url}/v1/vendor/get-all-vendors")
            response.raise_for_status() 
            if response.status_code == 200:
                data = response.json()
                if data.get("response_status"):
                    return Result.Ok(data=data.get("source_output"))
                else:
                    return Result.Fail(message=data.get("message", "An unknown error occurred."), code=response.status_code)
            else:
                return Result.Fail(message=f"HTTP error: {response.status_code} - {response.text}", code=response.status_code)
    except httpx.HTTPStatusError as e:
        return Result.Fail(message=f"HTTP error: {e.response.status_code} - {e.response.text}", code=e.response.status_code)
    except Exception as e:
        return Result.Fail(message=str(e))