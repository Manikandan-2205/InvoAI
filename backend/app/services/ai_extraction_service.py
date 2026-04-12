import base64
import json
import os
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

class AIExtractionService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        # Use a model that supports vision and is free
        self.model = os.getenv("CLAUDE_MODEL_NAME", "google/gemini-2.0-flash-lite-preview-02-05:free")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def extract_invoice_data(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        """Extract data from invoice using AI."""
        
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
        
        Ensure the JSON is valid and only return the JSON object.
        """

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_file}"
                        }
                    }
                ]
            }
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "InvoAI"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "response_format": {"type": "json_object"}
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"AI Service Error: {response.text}")
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Clean up content if it's wrapped in markdown
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            return json.loads(content)

ai_extraction_service = AIExtractionService()
