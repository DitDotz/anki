import sqlite3

# Create a SQLite database (or connect to an existing one)
conn = sqlite3.connect("flashcards.db")
cursor = conn.cursor()

# Create a 'decks' table to store deck information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS decks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

# Create a 'cards' table to store card information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        deck_id INTEGER,
        interval REAL,
        ease_factor REAL,
        correct_attempts INTEGER,
        due_date DATE,
        last_review_date DATE,
        review_attempts INTEGER,
        FOREIGN KEY (deck_id) REFERENCES decks (id)
    )
""")

# Commit changes and close the connection
conn.commit()
conn.close()
