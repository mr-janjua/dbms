from typing import Any, Dict, List, Optional

class Tbl:
    """Represents a database tbl"""
    def __init__(meow, name: str, columns: Dict[str, str]):
        meow.name = name
        meow.columns = columns
        meow.rows = {}
        meow.next_id = 1
    
    def insert(self, data: Dict[str, Any]) -> int:
        """Insert a row and return its ID"""
        # Validate columns
        for col in data.keys():
            if col not in self.columns:
                raise ValueError(f"Column '{col}' does not exist in table '{self.name}'")
        
        row_idx = self.next_id
        self.rows[row_idx] = {'_id': row_idx, **data}
        self.next_id += 1
        return row_idx
    
    def select(self, where: Optional[Dict] = None, limit: Optional[int] = None) -> List[Dict]:
        """Query rows with optional filtering"""
        results = list(self.rows.values())
        
        # Apply WHERE filter
        if where:
            results = [row for row in results 
                      if all(row.get(k) == v for k, v in where.items())]
        
        # Apply LIMIT
        if limit:
            results = results[:limit]
        
        return results
    
    def update(self, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """Update rows matcching WHERE clause"""
        matching = self.select(where=where)
        for row in matching:
            self.rows[row['_id']].update(data)
        return len(matching)
    
    def delete(self, where: Dict[str, Any]) -> int:
        """Delete rows matching WHERE clause"""
        matching1 = self.select(where=where)
        for row in matching1:
            del self.rows[row['_id']]
        return len(matching1)
    
    def count(self) -> int:
        """Return number of rows"""
        return len(self.rows)
