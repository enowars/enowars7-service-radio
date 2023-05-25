import sqlite3
import uuid
import os

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the database file
db_path = os.path.join(current_dir, "proposals.db")


def register_user(secret_key):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create a new table with two columns
    conn.execute(
        """CREATE TABLE IF NOT EXISTS my_table
             (id TEXT,
             value TEXT)"""
    )

    # Generate a new ID and insert it into the database
    new_id = str(uuid.uuid4())
    conn.execute("INSERT INTO my_table (id, value) VALUES (?, ?)", (new_id, secret_key))

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()
    return new_id


def validate_user(id):
    conn = sqlite3.connect(db_path)

    # Execute a query to retrieve the IDs from the database
    cursor = conn.execute("SELECT (?) FROM my_table", (id))
    ids = [row[0] for row in cursor]

    # Check if the provided ID exists in the database
    if id in ids:
        return True

    # Close the database connection
    conn.close()
    return False
