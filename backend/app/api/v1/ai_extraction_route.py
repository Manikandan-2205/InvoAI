from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_extraction_service import ai_extraction_service
import mimetypes

router = APIRouter()

@router.post("/extract")
async def extract_invoice_ai(file: UploadFile = File(...)):
    """Extract invoice data using AI via OpenRouter."""
    try:
        content = await file.read()
        mime_type = file.content_type or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
        
        # Only support common image/pdf formats for now
        if not mime_type.startswith('image/') and mime_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload an image or PDF.")
            
        data = await ai_extraction_service.extract_invoice_data(content, mime_type)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
