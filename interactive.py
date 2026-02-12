# ============ INTERACTIVE CLI ============

import os
from typing import List, Dict, Any
from typing import Optional
import json
from pydbms import PyDBMS


class DBMSCLI:
    """Interactive command-line interface for PyDBMS"""
    
    def __init__(self):
        self.db = None
        self.running = True
    
    def run(self):
        """Start the interactive CLI"""
        self.print_header()
        self.help()
        
        while self.running:
            try:
                command = input("\ndb> ").strip()
                if command:
                    self.execute_command(command)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def print_header(self):
        """Print CLI header"""
        print("=" * 70)
        print("PyDBMS - Simple Local Database Management System")
        print("=" * 70)
    
    def execute_command(self, command: str):
        """Execute a CLI command"""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == 'help':
            self.help()
        elif cmd == 'use':
            self.use_database(parts[1] if len(parts) > 1 else None)
        elif cmd == 'status':
            self.show_status()
        elif cmd == 'create':
            if len(parts) > 1 and parts[1].lower() == 'table':
                self.create_table_interactive()
            else:
                print("Usage: create table")
        elif cmd == 'drop':
            if len(parts) > 2 and parts[1].lower() == 'table':
                self.drop_table(parts[2])
            else:
                print("Usage: drop table <table_name>")
        elif cmd == 'show':
            if len(parts) > 1 and parts[1].lower() == 'tables':
                self.show_tables()
            elif len(parts) > 1 and parts[1].lower() == 'databases':
                self.show_databases()
            else:
                print("Usage: show tables | show databases")
        elif cmd == 'describe':
            if len(parts) > 1:
                self.describe_table(parts[1])
            else:
                print("Usage: describe <table_name>")
        elif cmd == 'view':
            if len(parts) > 1:
                self.view_table(parts[1])
            else:
                print("Usage: view <table_name>")
        elif cmd == 'insert':
            self.insert_interactive()
        elif cmd == 'select':
            self.select_interactive()
        elif cmd == 'update':
            self.update_interactive()
        elif cmd == 'delete':
            self.delete_interactive()
        elif cmd == 'export':
            self.export_interactive()
        elif cmd == 'import':
            self.import_interactive()
        elif cmd == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
        elif cmd == 'exit' or cmd == 'quit':
            self.running = False
            print("Goodbye! you noodle headed BALD SNOWFLAKE")
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")
    
# For the guy who asked for the code in the middle, here it is:
# Btw, many programmers are just snails with shell accounts, so no worries :)

    def help(self):
        """Show help menu"""
        print("\n" + "=" * 70)
        print("HELP MENU - CAUSE YOU ARE TOO DUMB TO GET IT ON YOUR OWN")
        print("=" * 70)
        print("\nDATABASE COMMANDS:")
        print("  use <database>       - Open/create a database")
        print("  status               - Show current database status")
        print("  show databases       - List all available databases")
        print("\nTABLE COMMANDS:")
        print("  create table         - Create a new table (interactive)")
        print("  drop table <name>    - Delete a table")
        print("  show tables          - List all tables")
        print("  describe <table>     - Show table structure")
        print("  view <table>         - Display all data in table")
        print("\nDATA COMMANDS:")
        print("  insert               - Insert data (interactive)")
        print("  select               - Query data (interactive)")
        print("  update               - Update data (interactive)")
        print("  delete               - Delete data (interactive)")
        print("\nIMPORT/EXPORT:")
        print("  export               - Export table to JSON")
        print("  import               - Import data from JSON")
        print("\nOTHER:")
        print("  help                 - Show this help menu")
        print("  clear                - Clear screen")
        print("  exit / quit          - Exit PyDBMS")
        print("=" * 70)
    
    def use_database(self, db_name: Optional[str]):
        """Open or create a database"""
        if not db_name:
            db_name = input("Database name: ").strip()
        
        self.db = PyDBMS(db_name)
        print(f"✓ Using database '{db_name}'")
        print(f"  Location: {self.db.db_path}")
        
        if self.db.list_tables():
            print(f"  Tables: {', '.join(self.db.list_tables())}")
        else:
            print("  No tables yet. Use 'create table' to get started.")
    
    def show_status(self):
        """Show current database status"""
        if not self.db:
            print("No database selected. Use 'use <database_name>'")
            return
        
        info = self.db.get_database_info()
        print("\n" + "=" * 70)
        print("DATABASE STATUS")
        print("=" * 70)
        print(f"Name: {info['name']}")
        print(f"Location: {info['path']}")
        print(f"Tables: {info['total_tables']}")
        print(f"Total Rows: {info['total_rows']}")
        
        if info['tables']:
            print("\nTables:")
            for table in info['tables']:
                table_info = self.db.describe(table)
                print(f"  • {table}: {table_info['row_count']} rows, {len(table_info['columns'])} columns")
        
        print("=" * 70)
    
    def show_databases(self):
        """Show all available databases"""
        if not os.path.exists('databases'):
            print("No databases found")
            return
        
        databases = [d for d in os.listdir('databases') 
                    if os.path.isdir(os.path.join('databases', d))]
        
        if databases:
            print("\nAvailable databases:")
            for db in databases:
                db_path = os.path.join('databases', db)
                metadata_file = os.path.join(db_path, 'metadata.json')
                
                if os.path.exists(metadata_file):
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        table_count = len(metadata.get('tables', {}))
                        print(f"  • {db} ({table_count} tables)")
                else:
                    print(f"  • {db}")
        else:
            print("No databases found")
    
    def create_table_interactive(self):
        """Interactive table creation"""
        if not self.db:
            print("Please use a database first: use <database_name>")
            return
        
        table_name = input("Table name: ").strip()
        print("\nDefine columns (type 'done' when finished):")
        print("Supported types: str, int, float, bool")
        
        columns = {}
        while True:
            col_name = input("  Column name (or 'done'): ").strip()
            if col_name.lower() == 'done':
                break
            
            if not col_name:
                continue
                
            col_type = input(f"  Type for '{col_name}': ").strip()
            if col_type not in ['str', 'int', 'float', 'bool']:
                print("  Invalid type. Use: str, int, float, or bool")
                continue
            
            columns[col_name] = col_type
        
        if not columns:
            print("Table must have at least one column")
            return
        
        self.db.create_table(table_name, columns)
        
        # Show the created table structure
        print("\nTable created with structure:")
        self.describe_table(table_name)
    
    def drop_table(self, table_name: str):
        """Drop a table"""
        if not self.db:
            print("Please use a database first")
            return
        
        confirm = input(f"Are you sure you want to drop '{table_name}'? (yes/no): ")
        if confirm.lower() == 'yes':
            self.db.drop_table(table_name)
    
    def show_tables(self):
        """Show all tables"""
        if not self.db:
            print("Please use a database first")
            return
        
        tables = self.db.list_tables()
        if tables:
            print("\n" + "=" * 70)
            print("TABLES")
            print("=" * 70)
            for table in tables:
                info = self.db.describe(table)
                print(f"\n{table}:")
                print(f"  Rows: {info['row_count']}")
                print(f"  Columns: {', '.join(info['columns'].keys())}")
            print("=" * 70)
        else:
            print("No tables in this database")
    
    def describe_table(self, table_name: str):
        """Describe table structure"""
        if not self.db:
            print("Please use a database first")
            return
        
        info = self.db.describe(table_name)
        print(f"\n" + "=" * 70)
        print(f"TABLE: {info['name']}")
        print("=" * 70)
        print(f"Rows: {info['row_count']}")
        print("\nColumns:")
        for col, col_type in info['columns'].items():
            print(f"  • {col} ({col_type})")
        print("=" * 70)
    
    def view_table(self, table_name: str):
        """View all data in a table"""
        if not self.db:
            print("Please use a database first")
            return
        
        results = self.db.select(table_name)
        
        if results:
            print(f"\n{table_name} ({len(results)} rows):")
            self._print_table(results)
        else:
            print(f"Table '{table_name}' is empty")
    
    def insert_interactive(self):
        """Interactive data insertion"""
        if not self.db:
            print("Please use a database first")
            return
        
        table_name = input("Table name: ").strip()
        info = self.db.describe(table_name)
        
        print(f"\nEnter values for each column:")
        data = {}
        for col, col_type in info['columns'].items():
            value = input(f"  {col} ({col_type}): ").strip()
            
            # Type conversion
            try:
                if col_type == 'int':
                    data[col] = int(value)
                elif col_type == 'float':
                    data[col] = float(value)
                elif col_type == 'bool':
                    data[col] = value.lower() in ['true', '1', 'yes']
                else:
                    data[col] = value
            except ValueError:
                print(f"  Invalid value for type {col_type}")
                return
        
        row_id = self.db.insert(table_name, data)
        print(f"✓ Inserted row with ID: {row_id}")
        
        # Show the updated table
        print("\nCurrent data:")
        self.view_table(table_name)
    
    def select_interactive(self):
        """Interactive data selection"""
        if not self.db:
            print("Please use a database first")
            return
        
        table_name = input("Table name: ").strip()
        
        # Optional WHERE clause
        use_where = input("Add WHERE condition? (yes/no): ").strip().lower()
        where = None
        if use_where == 'yes':
            col = input("  Column: ").strip()
            val = input("  Value: ").strip()
            where = {col: val}
        
        # Optional LIMIT
        limit_input = input("Limit results (press Enter for all): ").strip()
        limit = int(limit_input) if limit_input else None
        
        results = self.db.select(table_name, where=where, limit=limit)
        
        if results:
            print(f"\n{len(results)} row(s) found:")
            self._print_table(results)
        else:
            print("No results found")
    
    def update_interactive(self):
        """Interactive data update"""
        if not self.db:
            print("Please use a database first")
            return
        
        table_name = input("Table name: ").strip()
        
        # WHERE clause
        print("\nWHERE condition:")
        where_col = input("  Column: ").strip()
        where_val = input("  Value: ").strip()
        where = {where_col: where_val}
        
        # SET clause
        print("\nSET values:")
        set_col = input("  Column: ").strip()
        set_val = input("  New value: ").strip()
        data = {set_col: set_val}
        
        count = self.db.update(table_name, data, where)
        print(f"✓ Updated {count} row(s)")
        
        # Show updated data
        print("\nUpdated data:")
        self.view_table(table_name)
    
    def delete_interactive(self):
        """Interactive data deletion"""
        if not self.db:
            print("Please use a database first")
            return
        
        table_name = input("Table name: ").strip()
        
        # WHERE clause
        print("\nWHERE condition:")
        col = input("  Column: ").strip()
        val = input("  Value: ").strip()
        where = {col: val}
        
        confirm = input(f"\nDelete rows where {col}='{val}'? (yes/no): ")
        if confirm.lower() == 'yes':
            count = self.db.delete(table_name, where)
            print(f"✓ Deleted {count} row(s)")
            
            # Show remaining data
            print("\nRemaining data:")
            self.view_table(table_name)
    
    def export_interactive(self):
        """Interactive table export"""
        if not self.db:
            print("Please use a database first")
            return
        
        table_name = input("Table name: ").strip()
        filename = input("Export to file: ").strip()
        
        self.db.export_table(table_name, filename)
    
    def import_interactive(self):
        """Interactive table import"""
        if not self.db:
            print("Please use a database first")
            return
        
        table_name = input("Table name: ").strip()
        filename = input("Import from file: ").strip()
        
        self.db.import_table(table_name, filename)
        
        # Show imported data
        print("\nImported data:")
        self.view_table(table_name)
    
    def _print_table(self, rows: List[Dict]):
        """Pretty print table results"""
        if not rows:
            return
        
        # Get all columns
        columns = list(rows[0].keys())
        
        # Calculate column widths
        widths = {col: len(str(col)) for col in columns}
        for row in rows:
            for col in columns:
                widths[col] = max(widths[col], len(str(row.get(col, ''))))
        
        # Print separator
        separator = "  +" + "+".join("-" * (widths[col] + 2) for col in columns) + "+"
        print(separator)
        
        # Print header
        header = "  |" + "|".join(f" {col.ljust(widths[col])} " for col in columns) + "|"
        print(header)
        print(separator)
        
        # Print rows
        for row in rows:
            line = "  |" + "|".join(f" {str(row.get(col, '')).ljust(widths[col])} " for col in columns) + "|"
            print(line)
        
        print(separator)
