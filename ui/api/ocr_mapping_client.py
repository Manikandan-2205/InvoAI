import httpx
import os
from utils.result import Result

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api")

def process_ocr_mapping(file_content, filename, mapping_json):
    try:
        files = {'file': (filename, file_content)}
        data = {'mapping': mapping_json}
        with httpx.Client(verify=False, timeout=30.0) as client:
            response = client.post(f"{api_base_url}/v1/ocr/process-mapping", files=files, data=data)
            response.raise_for_status()
            
            data = response.json()
            if data.get("success"):
                return Result.Ok(data=data.get("results"))
            else:
                return Result.Fail(message=data.get("error", "OCR failed"))
    except Exception as e:
        return Result.Fail(message=str(e))
