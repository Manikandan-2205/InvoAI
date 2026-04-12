# InvoAI

## Overview
InvoAI is an AI-powered Invoice OCR Automation System built with Python. It extracts key details and tables from PDF or image invoices using OCR and machine learning, returning clean JSON via API with an interactive UI for visualization and validation.

## Key Features
- **AI-Powered OCR**: Extracts text and structured data from invoices
- **Table Recognition**: Identifies and parses invoice tables
- **API Service**: Returns structured JSON data from processed invoices
- **Interactive UI**: Allows users to review and validate extracted data

## Architecture
1. **Core Components**:
   - `app/core`: Handles configuration, logging, and database connections
   - `app/models`: Defines data models for invoices and entities
   - `app/repositories`: Implements data access layer using SQLAlchemy
   - `app/api`: Exposes RESTful endpoints for invoice processing

2. **Workflow**:
   - Ingest invoice (PDF/image)
   - OCR processing with ML models
   - Data validation and JSON structuring
   - API response with validation UI

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env` (database URL, etc.)
3. Initialize database with Alembic migrations
4. Run the API server

## API Documentation
Visit `/api/docs` for Swagger UI to explore endpoints like:
- `POST /api/v1/login` for user authentication
- `POST /api/v1/extract` for invoice processing

## Contributing
Follow standard GitFlow workflow. Pull requests welcome for features or bug fixes.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- OCR/AI libraries (specifics in codebase)