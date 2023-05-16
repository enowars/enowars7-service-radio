import sqlite3
import uuid


def register_user(secret_key):
    # Connect to the SQLite database
    conn = sqlite3.connect("authentication.db")

    # Create a new table with two columns
    conn.execute(
        """CREATE TABLE IF NOT EXISTS my_table
             (id TEXT,
             value TEXT)"""
    )

    # Generate a new ID and insert it into the database
    new_id = uuid.uuid4()
    conn.execute(
        "INSERT INTO my_table (id, value) VALUES (?, ?)", (str(new_id), secret_key)
    )

    # Commit the changes to the database
    conn.commit()

    # Retrieve the IDs from the database
    cursor = conn.execute("SELECT id FROM my_table")
    ids = [row[0] for row in cursor]

    print(ids)

    # Close the database connection
    conn.close()
    return new_id


def validate_user(id):
    conn = sqlite3.connect("authentication.db")
    # Retrieve the IDs from the database

    cursor = conn.execute("SELECT (?) FROM my_table", id)
    ids = [row[0] for row in cursor]
    if id in ids:
        return True
    return False
