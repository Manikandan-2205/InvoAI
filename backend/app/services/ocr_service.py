import pytesseract
from PIL import Image
import io
from typing import List, Dict, Any

class OCRService:
    @staticmethod
    def extract_from_regions(image_content: bytes, regions: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Extract text from specifically defined regions in an image.
        regions: [{'label': 'invoice_no', 'x': 10, 'y': 20, 'w': 100, 'h': 50}, ...]
        """
        image = Image.open(io.BytesIO(image_content))
        results = {}
        
        for region in regions:
            label = region.get('label', 'unknown')
            x = region.get('x', 0)
            y = region.get('y', 0)
            w = region.get('w', 10)
            h = region.get('h', 10)
            
            # Crop image (left, top, right, bottom)
            crop = image.crop((x, y, x + w, y + h))
            
            # Perform OCR on crop
            text = pytesseract.image_to_string(crop).strip()
            results[label] = text
            
        return results

ocr_service = OCRService()
