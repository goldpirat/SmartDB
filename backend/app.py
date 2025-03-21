import os
from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from dotenv import load_dotenv

# Import our models
from models.nlp.nl_to_sql import NLToSQLConverter
from models.image_processing.er_to_sql import ERToSQLConverter
from models.sql.sql_executor import SQLExecutor

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SmartDB Architect",
    description="AI-powered tool to convert natural language and ER diagrams into SQL code",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class NLQueryRequest(BaseModel):
    text_description: str
    db_engine: Optional[str] = "sqlite"  # Default to SQLite

class SQLRequest(BaseModel):
    sql_code: str
    db_engine: Optional[str] = "sqlite"

class SQLResponse(BaseModel):
    sql_code: str
    execution_log: Optional[str] = None
    error: Optional[str] = None
    results: Optional[list] = None

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to SmartDB Architect API"}

@app.post("/api/nl-to-sql", response_model=SQLResponse)
async def natural_language_to_sql(request: NLQueryRequest):
    """
    Convert natural language description to SQL code
    """
    try:
        # Initialize converter with requested DB engine
        converter = NLToSQLConverter(db_engine=request.db_engine)
        
        # Convert NL to SQL
        sql_code = converter.convert(request.text_description)
        
        return SQLResponse(sql_code=sql_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/er-to-sql", response_model=SQLResponse)
async def er_diagram_to_sql(
    file: UploadFile = File(...),
    db_engine: Optional[str] = Form("sqlite")
):
    """
    Convert ER diagram image to SQL code
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Initialize converter with requested DB engine
        converter = ERToSQLConverter(db_engine=db_engine)
        
        # Convert ER diagram to SQL
        sql_code = await converter.process_image(file_content)
        
        return SQLResponse(sql_code=sql_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute-sql", response_model=SQLResponse)
async def execute_sql(request: SQLRequest):
    """
    Execute the provided SQL code
    """
    try:
        # Initialize SQL executor
        executor = SQLExecutor(db_engine=request.db_engine)
        
        # Execute SQL
        result = executor.execute(request.sql_code)
        
        if result["success"]:
            return SQLResponse(
                sql_code=request.sql_code,
                execution_log=result.get("log", ""),
                results=result.get("results", [])
            )
        else:
            return SQLResponse(
                sql_code=request.sql_code,
                execution_log=result.get("log", ""),
                error=result.get("message", "Unknown error")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/schema")
async def get_schema(db_engine: Optional[str] = "sqlite"):
    """
    Get the current database schema
    """
    try:
        # Initialize SQL executor
        executor = SQLExecutor(db_engine=db_engine)
        
        # Connect to database
        executor.connect()
        
        # Get schema
        schema = executor.get_schema()
        
        if schema["success"]:
            return schema
        else:
            raise HTTPException(status_code=500, detail=schema.get("message", "Unknown error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for frontend
try:
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
except Exception as e:
    print(f"Warning: Could not mount frontend files. {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
