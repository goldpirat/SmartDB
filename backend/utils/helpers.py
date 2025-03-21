import os
import json
from typing import Dict, Any, List, Optional, Union
import re

def sanitize_table_name(name: str) -> str:
    """
    Sanitize table name to be SQL-compliant
    """
    # Remove spaces and special characters, replace with underscores
    name = re.sub(r'[^\w]', '_', name).lower()
    
    # Ensure it doesn't start with a number
    if name[0].isdigit():
        name = f"t_{name}"
        
    return name

def sanitize_column_name(name: str) -> str:
    """
    Sanitize column name to be SQL-compliant
    """
    # Remove spaces and special characters, replace with underscores
    name = re.sub(r'[^\w]', '_', name).lower()
    
    # Ensure it doesn't start with a number
    if name[0].isdigit():
        name = f"c_{name}"
        
    return name

def infer_sql_type(sample_value: Any) -> str:
    """
    Infer SQL type from a sample value
    """
    if isinstance(sample_value, int):
        return "INTEGER"
    elif isinstance(sample_value, float):
        return "REAL"
    elif isinstance(sample_value, bool):
        return "BOOLEAN"
    elif isinstance(sample_value, str):
        # Check if it looks like a date
        if re.match(r'\d{4}-\d{2}-\d{2}', sample_value):
            return "DATE"
        # Check if it looks like a timestamp
        elif re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', sample_value):
            return "TIMESTAMP"
        else:
            return "TEXT"
    else:
        return "TEXT"  # Default type

def parse_sql_error(error_message: str) -> Dict[str, Any]:
    """
    Parse SQL error message and return structured info
    """
    known_errors = {
        "UNIQUE constraint failed": {
            "type": "constraint_violation",
            "constraint": "unique",
            "fix_suggestion": "Ensure values in the specified column are unique"
        },
        "FOREIGN KEY constraint failed": {
            "type": "constraint_violation",
            "constraint": "foreign_key",
            "fix_suggestion": "Ensure referenced values exist in the parent table"
        },
        "NOT NULL constraint failed": {
            "type": "constraint_violation",
            "constraint": "not_null",
            "fix_suggestion": "Provide a non-NULL value for the specified column"
        },
        "syntax error": {
            "type": "syntax_error",
            "fix_suggestion": "Check SQL syntax for errors"
        }
    }
    
    for pattern, info in known_errors.items():
        if pattern in error_message:
            return {
                "message": error_message,
                "parsed": info
            }
    
    # Default case if no known pattern is found
    return {
        "message": error_message,
        "parsed": {
            "type": "unknown_error",
            "fix_suggestion": "Review the SQL and database schema"
        }
    }

def sql_to_visualization_data(tables: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert SQL schema info to a format suitable for visualization
    """
    nodes = []
    edges = []
    
    # Create nodes for each table
    for table in tables:
        table_name = table["name"]
        columns = table["columns"]
        foreign_keys = table.get("foreign_keys", [])
        
        # Create node for this table
        nodes.append({
            "id": table_name,
            "label": table_name,
            "type": "table",
            "columns": [
                {
                    "name": col["name"],
                    "type": col["type"],
                    "primary": col["is_primary_key"] if "is_primary_key" in col else False,
                    "nullable": not col["not_null"] if "not_null" in col else True
                } for col in columns
            ]
        })
        
        # Create edges for foreign keys
        for fk in foreign_keys:
            ref_table = fk.get("referenced_table")
            if ref_table:
                edges.append({
                    "id": f"{table_name}_to_{ref_table}",
                    "source": table_name,
                    "target": ref_table,
                    "label": f"{fk.get('from_column')} → {fk.get('to_column')}",
                    "type": "foreign_key"
                })
    
    return {
        "nodes": nodes,
        "edges": edges
    } 