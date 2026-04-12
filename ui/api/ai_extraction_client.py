import httpx
import os
from utils.result import Result

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api")

def extract_ai(file_content, filename):
    try:
        # Use httpx to forward the file to the FastAPI backend
        files = {'file': (filename, file_content)}
        with httpx.Client(verify=False, timeout=60.0) as client:
            # Note: the endpoint we created in FastAPI was /api/v1/ai/extract
            response = client.post(f"{api_base_url}/v1/ai/extract", files=files)
            response.raise_for_status()
            
            data = response.json()
            if data.get("success"):
                return Result.Ok(data=data.get("data"))
            else:
                return Result.Fail(message=data.get("error", "Extraction failed"))
    except Exception as e:
        return Result.Fail(message=str(e))
