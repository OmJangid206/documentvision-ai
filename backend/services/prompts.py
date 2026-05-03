DOCUMENT_PROMPT = """
    You are an intelligent document extraction system.
    Analyze the provided official identity document and extract structured information.

    STRICT RULES:
    1. Return ONLY valid JSON
    2. Do NOT return explanation
    3. Do NOT return markdown
    5. Missing fields must be null

    The document may be:
    - Aadhaar Card
    - PAN Card
    - Passport
    - Driving License
    - Voter ID
    - or similar government-issued identity documents

    Return ONLY valid JSON.

    Required fields:
    - full_name
    - date_of_birth
    - address
    - id_number
    - document_type
    - confidence_score

    Rules:
    - Detect document type automatically
    - If a field is missing, return null
    - Do not guess uncertain values
    - Do not return explanations
    - Do not return markdown

    Document Text:
    {extracted_text}
"""