# Document Verification System

## Project Overview

This project is an AI-powered **Document Verification System** built using **FastAPI (Backend)** and **Next.js (Frontend)**.

The system extracts and verifies information from uploaded documents such as:

- Aadhaar Card
- PAN Card
- Passport
- Driving License
- Other scanned PDF/Image documents

It uses:

- **OCR (Optical Character Recognition)** with Tesseract
- **LLM Processing** using Groq API
- **FastAPI** for backend APIs
- **Next.js** for frontend UI

The goal is to convert unstructured document text into structured JSON data for document verification, and automation systems.

---

# Setup Steps

## Clone Repository

```bash
git clone https://github.com/OmJangid206/documentvision-ai.git
```

---

# Backend Setup

## Go Inside Backend Folder

```bash
cd documentvision-ai/backend
```

### Create Virtual Environment

```bash
python3 -m venv .venv
```

### Activate Virtual Environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required System Installations

### Install Tesseract and Poppler

These are required for OCR text extraction from images and PDF files.

### macOS

```bash
brew install tesseract
brew install poppler
```

### Ubuntu / Linux

```bash
sudo apt update
sudo apt install tesseract-ocr poppler-utils
```

### Windows

- Install **Tesseract OCR**
- Install **Poppler for Windows**
- Add both to system PATH

---

## Run Backend Application

```bash
uvicorn main:app --reload
```

## Environment Variables

Create a `.env` file inside the `backend/` folder:

GROQ_API_KEY=your_groq_api_key_here

### How to Get Groq API Key

You can generate a free API key from the Groq Console:

https://console.groq.com/

### Steps

1. Sign up or Login to Groq  
2. Create a free developer account  
3. Generate a new API key  
4. Copy the API key  
5. Paste it inside your `.env` file  

### Example

GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

The project uses Groq Free Tier for development and assignment purposes, so no paid subscription is required.

Backend runs at:

```text
http://localhost:8000
```

### Sample API Testing (Postman / cURL)

You can use sample files from the `uploads/` folder for testing.

Example:

```bash
curl --location 'http://127.0.0.1:8000/upload-documents' \
--form 'files=@"/Users/omprakashjangid/Downloads/EAadhaar-om-prakash.pdf"' \
--form 'files=@"/Users/omprakashjangid/Downloads/Aadhar-unlocked.jpg"'
```

You can also test the same endpoint using Postman by uploading files from the `uploads/` folder inside `backend/` folder.

### API Endpoint

```text
POST /upload-documents
```

Swagger API Docs:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

## Open New Terminal and Go Inside Frontend Folder

```bash
cd documentvision-ai/frontend
```

### Install Frontend Dependencies

```bash
npm install
```

### Run Frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```
---

# Architecture Overview

## High-Level Flow

```text
User Uploads Document
        ↓
FastAPI API Receives File
        ↓
OCR Text Extraction (Tesseract)
        ↓
Raw Text Processing
        ↓
Groq LLM Structured Extraction
        ↓
JSON Response Generation
        ↓
Frontend Displays Final Results
```

---

# AI Approach

## Why OCR + LLM?

Most official documents are uploaded as scanned PDFs or images, which means the data is not directly machine-readable.

### Step 1: OCR (Tesseract)

Tesseract is used to extract raw text from:

- PDF files
- JPG
- PNG
- JPEG
- TIFF

This converts image-based content into plain text.

---

### Step 2: LLM Processing (Groq API)

The extracted raw text is sent to the Groq LLM, which:

- identifies important fields
- understands document structure
- extracts key values
- returns clean structured JSON

Required fields:

- full_name
- date_of_birth
- address
- id_number
- document_type
- confidence_score

If any field is missing, the model returns `null`.

---

## Why This Approach?

Traditional regex-based extraction fails when:

- OCR quality is poor
- document formats vary
- labels are inconsistent
- scanned documents contain noise

Using LLM improves flexibility, accuracy, and real-world handling.

This makes the system much more reliable for production-level document verification.

---

# Scaling Strategy

To support large-scale production usage, the system can be scaled using the following approach:

## 1. Background Processing

Instead of processing documents inside the API request, use:

- Celery
- Redis
- RabbitMQ

This allows async document processing and improves response speed.

---

## 2. Cloud File Storage

Instead of storing files locally in `/uploads`, use:

- AWS S3
- Google Cloud Storage
- Azure Blob Storage

This improves scalability and reliability.

---

## 3. Database Integration

Store extracted results in:

- PostgreSQL
- MongoDB

This helps with:

- document history
- verification logs
- audit tracking
- user management

---

## 4. Multiple Worker Services

Separate services for:

- OCR processing
- LLM extraction

This improves performance and fault isolation.

---


# Cost Estimation

## OCR Layer

### Using Tesseract OCR

**Cost per document:** Free

**Reason:**  
Tesseract is open-source and runs locally without API charges.

---

## PDF Processing

### Using Poppler + pdf2image

**Cost per document:** Free

**Reason:**  
Used locally for converting PDF pages into images before OCR.

---

## LLM Extraction

### Using Groq + Llama 3

### Development Phase

**Cost:** Free (Groq free developer tier)

### Production Scale

If migrated to paid APIs like OpenAI/Gemini:

**Approximate cost:**  
$0.001 – $0.01 per document

depending on model and token usage.

---

## Estimated Cost for 50 Documents

### Current Implementation

Very low / nearly free using Groq free tier

### Using Paid APIs

Approximately:

**$0.05 – $0.50 for 50 documents**

depending on model selection and prompt size.

---

## Cost Optimization Strategy

- Use OCR first to reduce LLM token usage
- Send only extracted text instead of full files
- Cache duplicate document results
- Retry only failed documents
- Process documents independently for better scaling

---
