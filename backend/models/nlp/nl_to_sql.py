import os
from typing import Dict, Any, List, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

class NLToSQLConverter:
    """
    Class to handle natural language to SQL conversion
    """
    def __init__(self, db_engine: str = "sqlite"):
        self.db_engine = db_engine
        
    def extract_entities(self, text_description: str) -> List[Dict[str, Any]]:
        """
        Extract entities, attributes, and relationships from text description
        """
        # Create prompt for entity extraction
        prompt = f"""
        Extract database entities, their attributes, and relationships from the following description.
        Format the output as a JSON structure.
        
        Description: {text_description}
        
        Expected format:
        {{
            "entities": [
                {{
                    "name": "entity_name",
                    "attributes": [
                        {{ "name": "attr_name", "type": "data_type", "is_primary_key": bool, "is_nullable": bool }}
                    ]
                }}
            ],
            "relationships": [
                {{
                    "entity1": "entity_name",
                    "entity2": "entity_name",
                    "type": "one_to_many|many_to_many|one_to_one",
                    "attributes": [optional attributes of the relationship]
                }}
            ]
        }}
        """
        
        # TODO: Call OpenAI API to get entities
        # This is a placeholder
        entities = [
            {
                "name": "users",
                "attributes": [
                    {"name": "id", "type": "INTEGER", "is_primary_key": True, "is_nullable": False},
                    {"name": "username", "type": "TEXT", "is_primary_key": False, "is_nullable": False},
                ]
            }
        ]
        
        relationships = []
        
        return {"entities": entities, "relationships": relationships}
        
    def generate_sql(self, entities_data: Dict[str, Any]) -> str:
        """
        Generate SQL code from extracted entities data
        """
        sql_code = ""
        
        # Generate CREATE TABLE statements
        for entity in entities_data.get("entities", []):
            sql_code += self._generate_create_table(entity)
            
        # Generate relationship tables/constraints
        for relationship in entities_data.get("relationships", []):
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
        elif rel_type in ["one_to_many", "one_to_one"]:
            # Create foreign key constraint
            # For one-to-one, additional unique constraint may be needed
            # This is a simplified implementation
            return ""
        
        return ""
        
    def convert(self, text_description: str) -> str:
        """
        Convert natural language description to SQL code
        """
        # Extract entities and relationships
        entities_data = self.extract_entities(text_description)
        
        # Generate SQL from structured data
        sql_code = self.generate_sql(entities_data)
        
        return sql_code 