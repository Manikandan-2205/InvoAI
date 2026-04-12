from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ocr_service import ocr_service
import json
from typing import List

router = APIRouter()

@router.post("/process-mapping")
async def process_mapping(
    file: UploadFile = File(...),
    mapping: str = Form(...) # JSON string of regions
):
    """Process an image using a coordinate mapping."""
    try:
        content = await file.read()
        try:
            regions = json.loads(mapping)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid mapping JSON")
            
        data = ocr_service.extract_from_regions(content, regions)
        return {"success": True, "results": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
