import sqlite3


DB_PATH = "database/estatepulse.db"


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS property_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_run_id TEXT NOT NULL,
    property_url TEXT NOT NULL,
    title TEXT,
    price REAL,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    neighborhood TEXT,
    bedrooms INTEGER,
    bathrooms REAL,
    sqft INTEGER,
    property_type TEXT,
    availability TEXT,
    scraped_at TEXT NOT NULL
)
""")


connection.commit()
connection.close()


print("Property snapshots table created successfully.")