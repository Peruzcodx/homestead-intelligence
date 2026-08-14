import sqlite3
from datetime import datetime

DB_PATH = "database/estatepulse.db"


def clean_price(value):
    if not value:
        return None

    value = value.replace("$", "").replace(",", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


def clean_bedrooms(value, title=None):
    if value:
        try:
            return int(float(value))
        except ValueError:
            pass

    if title and "studio" in title.lower():
        return 0

    return None
def clean_bathrooms(value):
    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_sqft(value):
    if not value:
        return None

    value = (
        value
        .replace(",", "")
        .replace("sq ft", "")
        .strip()
    )

    try:
        return int(float(value))
    except ValueError:
        return None

def save_property(property_data, scrape_run_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
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
            availability TEXT
        )
    """)

    price = clean_price(property_data["price"])

    bedrooms = clean_bedrooms(
        property_data["bedrooms"],
        property_data["title"]
    )

    bathrooms = clean_bathrooms(
        property_data["bathrooms"]
    )

    sqft = clean_sqft(
        property_data["sqft"]
    )

    # ========================================================
    # CURRENT PROPERTY
    # ========================================================

    cursor.execute("""
        INSERT OR REPLACE INTO properties (
            url,
            title,
            price,
            street,
            city,
            state,
            zip,
            neighborhood,
            bedrooms,
            bathrooms,
            sqft,
            property_type,
            availability
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        property_data["url"],
        property_data["title"],
        price,
        property_data["street"],
        property_data["city"],
        property_data["state"],
        property_data["zip"],
        property_data["neighborhood"],
        bedrooms,
        bathrooms,
        sqft,
        property_data["property_type"],
        property_data["availability"],
    ))

    # ========================================================
    # PROPERTY SNAPSHOT
    # ========================================================

    cursor.execute("""
        INSERT INTO property_snapshots (
            scrape_run_id,
            property_url,
            title,
            price,
            street,
            city,
            state,
            zip,
            neighborhood,
            bedrooms,
            bathrooms,
            sqft,
            property_type,
            availability,
            scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scrape_run_id,
        property_data["url"],
        property_data["title"],
        price,
        property_data["street"],
        property_data["city"],
        property_data["state"],
        property_data["zip"],
        property_data["neighborhood"],
        bedrooms,
        bathrooms,
        sqft,
        property_data["property_type"],
        property_data["availability"],
        scrape_run_id,
    ))

    connection.commit()
    connection.close()