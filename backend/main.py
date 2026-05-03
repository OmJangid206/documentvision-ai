"""
main.py

This module handles:
- API initialization
- CORS configuration
- File upload endpoints
- Document processing workflow

Workflow:
Upload File -> Save Locally -> OCR Extraction -> LLM Processing -> Structured JSON Response

Supported documents:
- Aadhaar Card
- PAN Card
- Passport
- Other official identity documents
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil

from services.document_processor import process_document_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create local storage directory for uploaded documents
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def ping() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: API status confirmation message.
    """
    return {"message": "DocuVision AI Backend Running"}


@app.post("/upload-documents")
async def upload_documents(
    files: List[UploadFile] = File(...)
) -> dict:
    """
    Upload and process one or multiple documents.

    Supported files:
    - Images (JPG, PNG, JPEG)
    - PDFs

    Each file is processed independently using:
    OCR -> AI Extraction -> Structured JSON

    Args:
        files (List[UploadFile]): List of uploaded documents.

    Returns:
        dict: success status and extracted document data.
    """
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save uploaded file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process document using OCR + LLM
        extracted = process_document_data(file_path)

        results.append({
            "file_name": file.filename,
            "extracted_data": extracted
        })

    return {
        "success": True,
        "results": results
    }