# SmartDB Architect Backend

The backend service for SmartDB Architect, powered by FastAPI and OpenAI.

## Overview

This backend provides API endpoints to:
- Convert natural language descriptions to SQL code
- Convert ER diagram images to SQL code
- Execute SQL code for database creation
- Retrieve schema information

## Directory Structure

```
backend/
├── app.py                # Main FastAPI application
├── requirements.txt      # Python dependencies
├── models/               # Core models
│   ├── nlp/              # Natural language processing modules
│   ├── image_processing/ # ER diagram processing modules
│   └── sql/              # SQL execution and manipulation modules
└── utils/                # Utility functions
```

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Start the server:
   ```
   uvicorn app:app --reload
   ```

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Natural Language to SQL
`POST /api/nl-to-sql`

Input:
```json
{
  "text_description": "Create a database for a blog with users, posts, and comments",
  "db_engine": "sqlite"
}
```

### ER Diagram to SQL
`POST /api/er-to-sql`

Form data:
- `file`: The ER diagram image file
- `db_engine`: The database engine (default: "sqlite")

### Execute SQL
`POST /api/execute-sql`

Input:
```json
{
  "sql_code": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);",
  "db_engine": "sqlite"
}
```

### Get Schema
`GET /api/schema?db_engine=sqlite`

## Development

- Backend uses FastAPI for a high-performance API with automatic documentation
- OpenAI's GPT models are used for natural language processing
- Computer vision libraries (OpenCV, PIL) are used for ER diagram analysis
- SQLAlchemy is used for database interactions
