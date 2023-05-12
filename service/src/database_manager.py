import sqlite3


def create_database():
    # Connect to the database.
    conn = sqlite3.connect("proposals.db")

    # Create a table to store mp3 files.
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS music (
        id INTEGER PRIMARY KEY,
        artist TEXT NOT NULL,
        title TEXT NOT NULL,
        binary BLOB NOT NULL,
        owner TEXT NOT NULL
    )
    """
    )

    # Commit changes to the database.
    conn.commit()
    print("create db")
    # Close the database connection.
    conn.close()


def add_to_database(artist, title, binary, user_id):
    # Connect to the database.
    conn = sqlite3.connect("music.db")

    # Insert the mp3 file into the table.
    conn.execute(
        "INSERT INTO music (artist, title, binary, user_id) VALUES (?, ?, ?, ?)",
        (artist, title, binary, user_id),
    )

    # Commit changes to the database.
    conn.commit()

    # Close the database connection.
    conn.close()


def search_binary_by_title(title, user_id):
    # Connect to the database.
    conn = sqlite3.connect("music.db")

    # Execute the query to search for the song by its title.
    cursor = conn.execute(
        "SELECT binary FROM music WHERE title=? AND user_id=?", (title, user_id)
    )

    # Get the binary value of the song.
    binary_value = cursor.fetchone()

    # Close the database connection.
    conn.close()

    # Return the binary value of the song.
    return binary_value[0] if binary_value else None
