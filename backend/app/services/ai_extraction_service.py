import base64
import json
import os
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

class AIExtractionService:
    def __init__(self):
        # Default to local Ollama if not specified, otherwise use .env
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1/chat/completions")
        # Use a model that supports vision (e.g., llava, llama3.2-vision)
        self.model = os.getenv("OLLAMA_VISION_MODEL", "llama3.2-vision")

    async def extract_invoice_data(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        """Extract data from invoice using Local Ollama AI."""
        
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

        # Ollama supports the OpenAI-style vision messages
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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "format": "json", # Ollama specific for raw JSON output
                    "stream": False
                },
                timeout=120.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Local AI Service (Ollama) Error: {response.text}")
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Clean up content if it's wrapped in markdown
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            return json.loads(content)

ai_extraction_service = AIExtractionService()
