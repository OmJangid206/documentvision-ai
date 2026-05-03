"""
document_extractor.py

This module provides functionality to extract text from PDF and image files
using Optical Character Recognition (OCR).
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_document(file_path: str) -> str:
    """
    Extract text content from a PDF or image file using OCR.

    This function supports:
    - PDF files: Converts each page into an image and extracts text using OCR.
    - Image files (JPG, PNG, JPEG, etc.): Directly extracts text using OCR.

    Args: 
        file_path (str):The full path to the input file (PDF or image).

    Returns:
        str: The extracted text content from the document.
    """
    extracted_text = ""

    # Process PDF files
    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path, dpi=300)

        for page in pages:
            extracted_text += pytesseract.image_to_string(page) + "\n"

    # Process image files
    else:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)

    return extracted_text