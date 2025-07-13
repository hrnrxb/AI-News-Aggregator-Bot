import sqlite3

# Define the database file name
DB_FILE = "sent_links.db"

def initialize_db():
    """
    Initializes the SQLite database and creates the 'sent' table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sent (
            link TEXT PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database '{DB_FILE}' initialized and 'sent' table ensured.")

def load_sent_links():
    """
    Loads all previously sent links from the database.
    Returns them as a set for efficient lookup.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM sent")
    links = {row[0] for row in cursor.fetchall()}
    conn.close()
    print(f"Loaded {len(links)} previously sent links from DB.")
    return links

def save_sent_link(link):
    """
    Saves a new link to the database. Ignores if the link already exists.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sent (link) VALUES (?)", (link,))
        conn.commit()
    except sqlite3.IntegrityError:
        # This means the link (PRIMARY KEY) already exists, so we ignore.
        pass
    finally:
        conn.close()
