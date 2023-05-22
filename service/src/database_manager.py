import sqlite3
import uuid
import os

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the database file
db_path = os.path.join(current_dir, "proposals.db")
print("TOMER", db_path)

# Function to remove invalid title chars, like "-"
remove_invalid_chars = (
    lambda s, chars, new_char: s[: min(s.index(c) for c in chars if c in s)]
    + new_char
    + s[min(s.index(c) for c in chars if c in s) + 1 :]
    if any(c in s for c in chars)
    else s
)


def create_database():
    # Connect to the database.
    conn = sqlite3.connect(db_path)

    # Create a table to store mp3 files.
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS music (
        id INTEGER PRIMARY KEY,
        artist TEXT NOT NULL,
        title TEXT NOT NULL,
        binary BLOB NOT NULL)
    """
    )

    # Commit changes to the database.
    conn.commit()
    print("create db")
    # Close the database connection.
    conn.close()


def add_to_database(artist, title, binary):
    # Connect to the database.
    conn = sqlite3.connect(db_path)

    # Generate a new ID and insert it into the database
    new_id = uuid.uuid4()
    # Insert the mp3 file into the table.
    conn.execute(
        "INSERT INTO music (artist, title, binary) VALUES (?, ?, ?)",
        (artist, title, binary),
    )

    # Commit changes to the database.
    conn.commit()

    # Close the database connection.
    conn.close()


def search_artist_by_title(title):
    # Connect to the database.
    conn = sqlite3.connect(db_path)
    title = remove_invalid_chars(title, ['"', "'", "-"], "")
    print(title)
    # Execute the query to search for the song by its title.
    cursor = conn.execute("SELECT artist FROM music WHERE title LIKE '%" + title + "%'")

    # Get all artists who have a song title like that.
    artist_value = cursor.fetchall()
    # Close the database connection.
    conn.close()

    # Return artist if exists.
    return artist_value if artist_value else None
