import os
import sqlite3
import tempfile
from typing import Dict, Any, List, Optional, Tuple

class SQLExecutor:
    """
    Class to handle SQL execution
    """
    def __init__(self, db_engine: str = "sqlite"):
        self.db_engine = db_engine
        self.db_connection = None
        self.temp_db_file = None
        
    def connect(self, db_name: str = None) -> bool:
        """
        Connect to a database
        """
        try:
            if self.db_engine == "sqlite":
                if db_name:
                    # Connect to specified database
                    self.db_connection = sqlite3.connect(db_name)
                else:
                    # Create a temporary database
                    self.temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
                    self.db_connection = sqlite3.connect(self.temp_db_file.name)
                
                # Enable foreign keys
                self.db_connection.execute("PRAGMA foreign_keys = ON")
                
                return True
            else:
                # TODO: Implement other database engines (MySQL, PostgreSQL, etc.)
                raise NotImplementedError(f"Database engine {self.db_engine} not implemented yet")
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """
        Disconnect from the database
        """
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
            
        # Remove temporary database file if it exists
        if self.temp_db_file and os.path.exists(self.temp_db_file.name):
            os.unlink(self.temp_db_file.name)
            self.temp_db_file = None
    
    def execute(self, sql_code: str) -> Dict[str, Any]:
        """
        Execute SQL code and return results
        """
        if not self.db_connection:
            connected = self.connect()
            if not connected:
                return {"success": False, "message": "Failed to connect to database", "log": ""}
        
        cursor = self.db_connection.cursor()
        results = []
        log = []
        
        try:
            # Split SQL code into individual statements
            statements = self._split_sql_statements(sql_code)
            
            for stmt in statements:
                if not stmt.strip():
                    continue
                    
                try:
                    cursor.execute(stmt)
                    
                    # If the statement is a SELECT, fetch results
                    if stmt.strip().upper().startswith("SELECT"):
                        columns = [desc[0] for desc in cursor.description]
                        rows = cursor.fetchall()
                        
                        results.append({
                            "columns": columns,
                            "rows": rows
                        })
                        
                        log.append(f"Successfully executed: {stmt[:50]}{'...' if len(stmt) > 50 else ''}")
                        log.append(f"Retrieved {len(rows)} rows")
                    else:
                        log.append(f"Successfully executed: {stmt[:50]}{'...' if len(stmt) > 50 else ''}")
                except Exception as e:
                    log.append(f"Error executing statement: {stmt[:50]}{'...' if len(stmt) > 50 else ''}")
                    log.append(f"Error message: {str(e)}")
                    
                    # Don't commit and return error
                    return {"success": False, "message": str(e), "log": "\n".join(log)}
            
            # Commit changes
            self.db_connection.commit()
            
            return {
                "success": True, 
                "message": "SQL execution completed successfully", 
                "log": "\n".join(log),
                "results": results
            }
        except Exception as e:
            return {"success": False, "message": str(e), "log": "\n".join(log)}
    
    def _split_sql_statements(self, sql_code: str) -> List[str]:
        """
        Split SQL code into individual statements
        """
        # Simple splitting by semicolon - more complex parsing might be needed
        # for real-world SQL with triggers, procedures, etc.
        statements = []
        current_statement = ""
        
        for line in sql_code.split("\n"):
            line = line.strip()
            
            # Skip comments
            if line.startswith("--") or line.startswith("#") or not line:
                continue
                
            current_statement += " " + line
            
            if line.endswith(";"):
                statements.append(current_statement.strip())
                current_statement = ""
        
        # Add the last statement if it doesn't end with semicolon
        if current_statement.strip():
            statements.append(current_statement.strip())
            
        return statements
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the current database schema
        """
        if not self.db_connection:
            return {"success": False, "message": "Not connected to a database"}
            
        cursor = self.db_connection.cursor()
        tables = []
        
        try:
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            table_names = [row[0] for row in cursor.fetchall()]
            
            for table_name in table_names:
                # Get table columns
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = []
                
                for col in cursor.fetchall():
                    columns.append({
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "is_primary_key": bool(col[5])
                    })
                
                # Get foreign keys
                cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                foreign_keys = []
                
                for fk in cursor.fetchall():
                    foreign_keys.append({
                        "id": fk[0],
                        "seq": fk[1],
                        "referenced_table": fk[2],
                        "from_column": fk[3],
                        "to_column": fk[4],
                        "on_update": fk[5],
                        "on_delete": fk[6],
                        "match": fk[7]
                    })
                
                tables.append({
                    "name": table_name,
                    "columns": columns,
                    "foreign_keys": foreign_keys
                })
            
            return {
                "success": True,
                "tables": tables
            }
        except Exception as e:
            return {"success": False, "message": str(e)} 