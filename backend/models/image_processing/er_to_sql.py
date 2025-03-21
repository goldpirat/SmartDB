import os
import io
from typing import Dict, Any, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

class ERToSQLConverter:
    """
    Class to handle ER diagram to SQL conversion
    """
    def __init__(self, db_engine: str = "sqlite"):
        self.db_engine = db_engine
        
    async def process_image(self, file_content: bytes) -> str:
        """
        Process the ER diagram image and generate SQL
        """
        # Convert bytes to image
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to OpenCV format for processing
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Preprocess image (can be expanded)
        preprocessed_img = self._preprocess_image(img_cv)
        
        # Extract image features using AI
        schema_data = await self._extract_schema_from_image(image)
        
        # Generate SQL from schema data
        sql_code = self._generate_sql(schema_data)
        
        return sql_code
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess the image for better feature extraction
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply thresholding to get binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        return thresh
    
    async def _extract_schema_from_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract database schema from ER diagram using AI
        """
        # Convert image to format suitable for API
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # TODO: Implement actual AI call for image analysis
        # This is a placeholder - in actual implementation, would use OpenAI Vision API
        # or other image analysis capabilities
        
        # Placeholder schema data
        schema_data = {
            "entities": [
                {
                    "name": "product",
                    "attributes": [
                        {"name": "id", "type": "INTEGER", "is_primary_key": True, "is_nullable": False},
                        {"name": "name", "type": "TEXT", "is_primary_key": False, "is_nullable": False},
                        {"name": "price", "type": "REAL", "is_primary_key": False, "is_nullable": True}
                    ]
                },
                {
                    "name": "category",
                    "attributes": [
                        {"name": "id", "type": "INTEGER", "is_primary_key": True, "is_nullable": False},
                        {"name": "name", "type": "TEXT", "is_primary_key": False, "is_nullable": False}
                    ]
                }
            ],
            "relationships": [
                {
                    "entity1": "product",
                    "entity2": "category",
                    "type": "many_to_one",
                    "attributes": []
                }
            ]
        }
        
        return schema_data
    
    def _generate_sql(self, schema_data: Dict[str, Any]) -> str:
        """
        Generate SQL from extracted schema data
        """
        sql_code = "-- SQL Generated from ER Diagram\n\n"
        
        # Generate CREATE TABLE statements for entities
        for entity in schema_data.get("entities", []):
            sql_code += self._generate_create_table(entity)
        
        # Generate relationship constraints
        for relationship in schema_data.get("relationships", []):
            sql_code += self._generate_relationship(relationship)
        
        return sql_code
    
    def _generate_create_table(self, entity: Dict[str, Any]) -> str:
        """Generate CREATE TABLE statement for an entity"""
        table_name = entity["name"]
        attributes = entity["attributes"]
        
        create_statement = f"CREATE TABLE {table_name} (\n"
        
        # Add columns
        columns = []
        primary_keys = []
        
        for attr in attributes:
            column_def = f"    {attr['name']} {attr['type']}"
            
            if not attr.get("is_nullable", True):
                column_def += " NOT NULL"
                
            if attr.get("is_primary_key", False):
                primary_keys.append(attr['name'])
                
            columns.append(column_def)
        
        # Add primary key constraint if specified
        if primary_keys:
            pk_constraint = f"    PRIMARY KEY ({', '.join(primary_keys)})"
            columns.append(pk_constraint)
            
        create_statement += ",\n".join(columns)
        create_statement += "\n);\n\n"
        
        return create_statement
    
    def _generate_relationship(self, relationship: Dict[str, Any]) -> str:
        """Generate SQL for relationships"""
        rel_type = relationship.get("type", "")
        entity1 = relationship.get("entity1", "")
        entity2 = relationship.get("entity2", "")
        
        if rel_type == "many_to_many":
            # Create junction table
            table_name = f"{entity1}_{entity2}"
            sql = f"CREATE TABLE {table_name} (\n"
            sql += f"    {entity1}_id INTEGER NOT NULL,\n"
            sql += f"    {entity2}_id INTEGER NOT NULL,\n"
            sql += f"    PRIMARY KEY ({entity1}_id, {entity2}_id),\n"
            sql += f"    FOREIGN KEY ({entity1}_id) REFERENCES {entity1} (id),\n"
            sql += f"    FOREIGN KEY ({entity2}_id) REFERENCES {entity2} (id)\n"
            sql += ");\n\n"
            return sql
        elif rel_type == "many_to_one":
            # Add foreign key to the "many" side
            sql = f"-- Add foreign key to implement {entity1} to {entity2} relationship\n"
            sql += f"ALTER TABLE {entity1} ADD COLUMN {entity2}_id INTEGER;\n"
            sql += f"ALTER TABLE {entity1} ADD FOREIGN KEY ({entity2}_id) REFERENCES {entity2} (id);\n\n"
            return sql
        elif rel_type == "one_to_one":
            # Implement one-to-one relationship with foreign key and unique constraint
            sql = f"-- Add foreign key with unique constraint for one-to-one relationship\n"
            sql += f"ALTER TABLE {entity1} ADD COLUMN {entity2}_id INTEGER UNIQUE;\n"
            sql += f"ALTER TABLE {entity1} ADD FOREIGN KEY ({entity2}_id) REFERENCES {entity2} (id);\n\n"
            return sql
        
        return "" 