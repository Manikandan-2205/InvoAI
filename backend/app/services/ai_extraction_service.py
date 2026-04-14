import base64
import json
import os
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

class AIExtractionService:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_VISION_MODEL", "deepseek-coder:1.3b")

    async def extract_invoice_data(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        """Extract data from invoice using AI via Ollama."""
        
        # Convert image/pdf to base64
        base64_file = base64.b64encode(file_content).decode('utf-8')
        
        prompt = """
        Extract the following information from this invoice/bill and return it as a JSON object:
        - invoice_number
        - invoice_date
        - vendor_name
        - vendor_address
        - customer_name
        - items (list of {description, quantity, unit_price, total})
        - subtotal
        - tax_amount
        - total_amount
        - currency
        
        Return ONLY valid JSON.
        """

        # Ollama native chat API format
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [base64_file] if mime_type.startswith('image/') else []
                }
            ],
            "stream": False,
            "format": "json"
        }

        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.host}/api/chat",
                headers=headers,
                json=payload,
                timeout=120.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama Service Error: {response.text}")
            
            result = response.json()
            content = result['message']['content']
            
            return json.loads(content)

ai_extraction_service = AIExtractionService()
