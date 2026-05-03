"""
document_processor.py

This module handles document data extraction by combining OCR text extraction
with AI-powered structured data parsing.
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv


from services.document_extractor import extract_text_from_document
from services.prompts import DOCUMENT_PROMPT
from schemas.schemas import ExtractedDocumentData

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def process_document_data(file_path: str) -> dict:
    """
    Extract structured data from a PDF or image document using OCR and LLM.

    Args:
        file_path (str): Path to the input document file.

    Returns:
        dict: Extracted fields including:
            full_name, date_of_birth, address,
            id_number, document_type, and confidence_score.
            Returns error details if processing fails.
    """
    if not GROQ_API_KEY:
        return {
            "success": False,
            "error": "GROQ_API_KEY is missing. Please add it to your .env file."
        }
        
    # Create client
    client = Groq(api_key=GROQ_API_KEY)
    
    extracted_text = extract_text_from_document(file_path)
    prompt = DOCUMENT_PROMPT.format(extracted_text=extracted_text)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        # Remove markdown formatting if present
        content = content.strip()
        content = content.replace("```json", "").replace("```", "")
        content = content.split("\n\n")[0]
        parsed_data = json.loads(content)
        validated_data = ExtractedDocumentData(**parsed_data)
        return validated_data.dict()

    except Exception as error:
        return {
            "error": str(error),
            "raw_text": extracted_text
        }
