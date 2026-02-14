"""
PyDBMS - Simple but Functional Local Database Management System
Features: Robust storage, visual table display, data verification
"""
# Issues at hand:
# Update wont work well
# Select isnt working well with where clause

import json
import os
import pickle
from typing import Any, Dict, List, Optional
from datetime import datetime

from table import Tbl
from interactive import DBMSCLI

class PyDBMS:
    """Simple, yet functional database management system"""
    
    def __init__(self, db_name: str = 'default'):
        self.db_name = db_name
        self.db_path = os.path.join('databases', db_name)
        self.tables = {}
        
        # Create database directory if it doesn't exist
        os.makedirs(self.db_path, exist_ok=True)
        
        # Load existing database
        self._load()
        
        # Save metadata
        self._save_metadata()
    
    # ============ TABLE OPERATIONS ============
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create a new table"""
        if table_name in self.tables:
            raise ValueError(f"Table '{table_name}' already exists")
        
        if not columns:
            raise ValueError("Table must have at least one column")
        
        self.tables[table_name] = Tbl(table_name, columns)
        self._save()
        self._save_metadata()
        print(f"✓ Tbl '{table_name}' created successfully")
        print(f"  Location: {self.db_path}")
    
    def drop_table(self, table_name: str) -> None:
        """Delete a table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        del self.tables[table_name]
        self._save()
        self._save_metadata()
        print(f"✓ Table '{table_name}' dropped successfully")
    
    def list_tables(self) -> List[str]:
        """List all tables"""
        return list(self.tables.keys())
    
    def describe(self, table_name: str) -> Dict:
        """Show table structure"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        table = self.tables[table_name]
        return {
            'name': table.name,
            'columns': table.columns,
            'row_count': table.count()
        }
    
    # ============ DATA OPERATIONS ============
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """Insert a row into table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        row_id = self.tables[table_name].insert(data)
        self._save()
        return row_id
    
    def select(self, table_name: str, where: Optional[Dict] = None, 
               limit: Optional[int] = None) -> List[Dict]:
        """Query data from table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        return self.tables[table_name].select(where=where, limit=limit)
    
    def update(self, table_name: str, data: Dict[str, Any], 
               where: Dict[str, Any]) -> int:
        """Update rows in table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        count = self.tables[table_name].update(data, where)
        self._save()
        return count
    
    def delete(self, table_name: str, where: Dict[str, Any]) -> int:
        """Delete rows from table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        count = self.tables[table_name].delete(where)
        self._save()
        return count
    
    # ============ PERSISTENCE ============
    
    def _save(self) -> None:
        """Save database to disk"""
        db_file = os.path.join(self.db_path, 'database.pkl')
        try:
            with open(db_file, 'wb') as f:
                pickle.dump(self.tables, f)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def _load(self) -> None:
        """Load database from disk"""
        db_file = os.path.join(self.db_path, 'database.pkl')
        if os.path.exists(db_file):
            try:
                with open(db_file, 'rb') as f:
                    self.tables = pickle.load(f)
            except Exception as e:
                print(f"Error loading database: {e}")
                self.tables = {}
    
    def _save_metadata(self) -> None:
        """Save database metadata as JSON for easy inspection"""
        metadata = {
            'database_name': self.db_name,
            'created': datetime.now().isoformat(),
            'tables': {}
        }
        
        for table_name, table in self.tables.items():
            metadata['tables'][table_name] = {
                'columns': table.columns,
                'row_count': table.count()
            }
        
        metadata_file = os.path.join(self.db_path, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    # ============ UTILITY ============
    
    def export_table(self, table_name: str, filename: str) -> None:
        """Export table to JSON file"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        data = self.select(table_name)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Exported {len(data)} rows to '{filename}'")
    
    def import_table(self, table_name: str, filename: str) -> None:
        """Import data from JSON file"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        count = 0
        for row in data:
            # Remove _id if present
            row.pop('_id', None)
            self.insert(table_name, row)
            count += 1
        
        print(f"✓ Imported {count} rows into '{table_name}'")
    
    def get_database_info(self) -> Dict:
        """Get complete database information"""
        return {
            'name': self.db_name,
            'path': self.db_path,
            'tables': list(self.tables.keys()),
            'total_tables': len(self.tables),
            'total_rows': sum(table.count() for table in self.tables.values())
        }

# ============ MAIN ENTRY POINT ============

if __name__ == '__main__':
    cli = DBMSCLI()
    cli.run()