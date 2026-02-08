import sqlite3

# Connect to the database
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables in database:', tables)

# Get schema for each table
for table_name, in tables:
    print(f'\nSchema for table: {table_name}')
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for col in columns:
        cid, name, type_, notnull, default_value, pk = col
        print(f"  Column: {name}, Type: {type_}, Not Null: {bool(notnull)}, PK: {bool(pk)}")

# Also check a sample of the tasks table if it exists
if ('tasks',) in tables:
    print('\nSample data from tasks table:')
    cursor.execute("SELECT * FROM tasks LIMIT 3;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  Row: {row}")

conn.close()