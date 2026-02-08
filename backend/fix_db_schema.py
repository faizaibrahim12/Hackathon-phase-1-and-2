"""
Script to fix the user_id column type in the tasks table
Since SQLite doesn't support ALTER COLUMN, we need to recreate the table
"""
import sqlite3

def fix_user_id_type():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    print("Backing up current tasks table...")
    
    # Get all data from the current tasks table
    cursor.execute("SELECT * FROM tasks;")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} rows in tasks table")
    
    # Store the data temporarily
    temp_tasks = []
    for row in rows:
        task_id, user_id, title, description, completed, due_date, created_at, updated_at = row
        # Convert user_id to string to match the expected format
        temp_tasks.append((task_id, str(user_id), title, description, completed, due_date, created_at, updated_at))
    
    # Drop the current tasks table
    cursor.execute("DROP TABLE tasks;")
    
    # Recreate the tasks table with user_id as TEXT (which will store strings)
    cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(5000),
            completed BOOLEAN NOT NULL DEFAULT 0,
            due_date DATE,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        );
    """)
    
    # Recreate the index
    cursor.execute("CREATE INDEX ix_tasks_user_id ON tasks (user_id);")
    cursor.execute("CREATE INDEX ix_tasks_completed ON tasks (completed);")
    cursor.execute("CREATE INDEX ix_tasks_created_at ON tasks (created_at);")
    
    # Insert the data back with user_id as string
    for task_row in temp_tasks:
        cursor.execute("""
            INSERT INTO tasks (id, user_id, title, description, completed, due_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, task_row)
    
    print("Tasks table recreated with user_id as TEXT type")
    
    # Also fix the 'task' table if it exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task';")
    if cursor.fetchone():
        print("Fixing 'task' table as well...")
        
        # Get data from 'task' table
        cursor.execute("SELECT * FROM task;")
        task_rows = cursor.fetchall()
        
        temp_task_rows = []
        for row in task_rows:
            task_id, user_id, title, description, completed, due_date, created_at, updated_at = row
            temp_task_rows.append((task_id, str(user_id), title, description, completed, due_date, created_at, updated_at))
        
        # Drop and recreate 'task' table
        cursor.execute("DROP TABLE task;")
        
        cursor.execute("""
            CREATE TABLE task (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0,
                due_date DATE,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            );
        """)
        
        # Recreate the index
        cursor.execute("CREATE INDEX ix_task_user_id ON task (user_id);")
        cursor.execute("CREATE INDEX ix_task_completed ON task (completed);")
        cursor.execute("CREATE INDEX ix_task_created_at ON task (created_at);")
        
        # Insert data back
        for task_row in temp_task_rows:
            cursor.execute("""
                INSERT INTO task (id, user_id, title, description, completed, due_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, task_row)
        
        print("'task' table recreated with user_id as TEXT type")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("Database schema updated successfully!")

if __name__ == "__main__":
    fix_user_id_type()