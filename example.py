"""
This is the example file for PyDBMS. It demonstrates how data is stored and displayed when using the PyDBMS library.
"""

from pydbms import PyDBMS
import os

print("=" * 70)
print("PyDBMS - This shows how data is stored and displayed")
print("=" * 70)

# Example 1: Create database and verify storage
print("\n1. Creating 'shop' database...")
db = PyDBMS('shop')

print("\n2. Creating 'products' table...")
db.create_table('products', {
    'name': 'str',
    'price': 'float',
    'stock': 'int'
})

print("\n3. Adding products...")
db.insert('products', {'name': 'Laptop', 'price': 999.99, 'stock': 50})
db.insert('products', {'name': 'Mouse', 'price': 29.99, 'stock': 200})
db.insert('products', {'name': 'Keyboard', 'price': 79.99, 'stock': 150})

print("\n4. Displaying all products:")
products = db.select('products')
print("\n  Data structure:")
for product in products:
    print(f"    {product}")

print("\n5. Checking storage location:")
print(f"    Database path: {db.db_path}")
print(f"    Files exist: {os.path.exists(db.db_path)}")

db_file = os.path.join(db.db_path, 'database.pkl')
metadata_file = os.path.join(db.db_path, 'metadata.json')
print(f"    database.pkl: {os.path.exists(db_file)}")
print(f"    metadata.json: {os.path.exists(metadata_file)}")

# Example 2: Get database info
print("\n6. Database information:")
info = db.get_database_info()
print(f"    Name: {info['name']}")
print(f"    Tables: {info['total_tables']}")
print(f"    Total rows: {info['total_rows']}")

# Example 3: Table operations
print("\n7. Updating product stock...")
db.update('products', {'stock': 45}, where={'name': 'Laptop'})

print("\n8. Finding products:")
laptop = db.select('products', where={'name': 'Laptop'})
print(f"    Laptop stock: {laptop[0]['stock']}")

# Example 4: Show what persistence looks like
print("\n9. Simulating program restart...")
print("    Closing database...")
del db

print("    Opening database again...")
db2 = PyDBMS('shop')

print("\n10. Verifying data persisted:")
products_after = db2.select('products')
print(f"    Found {len(products_after)} products after 'restart'")
for p in products_after:
    print(f"    - {p['name']}: ${p['price']} ({p['stock']} in stock)")

print("\n" + "=" * 70)
print("Example complete!")
print("=" * 70)
print("\nYour data is stored in: databases/shop/")
print("Try these commands:")
print("  1. Run: python pydbms.py")
print("  2. Type: use shop")
print("  3. Type: view products")
print("  4. You'll see all your data!")
print("\nTo clean up: rm -rf databases/shop")
