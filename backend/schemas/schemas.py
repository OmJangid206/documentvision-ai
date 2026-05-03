"""
schemas.py

Pydantic models for structured document extraction response.
"""

from pydantic import BaseModel
from typing import Optional


class ExtractedDocumentData(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    id_number: Optional[str] = None
    document_type: Optional[str] = None
    confidence_score: Optional[float] = None