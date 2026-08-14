import sqlite3
from datetime import datetime


DB_PATH = "database/estatepulse.db"


def create_change_events_table():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS change_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scrape_run_id TEXT NOT NULL,
            property_url TEXT NOT NULL,
            title TEXT,
            change_type TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            change_amount REAL,
            detected_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_change_events(changes):

    create_change_events_table()

    scrape_run_id = changes["latest_scrape"]

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    detected_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------------------------
    # NEW LISTINGS
    # --------------------------------------------------------

    for change in changes["new_listings"]:

        cursor.execute("""
            INSERT INTO change_events (
                scrape_run_id,
                property_url,
                title,
                change_type,
                old_value,
                new_value,
                change_amount,
                detected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scrape_run_id,
            change["url"],
            change["title"],
            "NEW_LISTING",
            None,
            change["availability"],
            None,
            detected_at,
        ))

    # --------------------------------------------------------
    # PRICE CHANGES
    # --------------------------------------------------------

    for change in changes["price_changes"]:

        cursor.execute("""
            INSERT INTO change_events (
                scrape_run_id,
                property_url,
                title,
                change_type,
                old_value,
                new_value,
                change_amount,
                detected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scrape_run_id,
            change["url"],
            change["title"],
            "PRICE",
            str(change["old_price"]),
            str(change["new_price"]),
            change["change"],
            detected_at,
        ))

    # --------------------------------------------------------
    # AVAILABILITY CHANGES
    # --------------------------------------------------------

    for change in changes["availability_changes"]:

        cursor.execute("""
            INSERT INTO change_events (
                scrape_run_id,
                property_url,
                title,
                change_type,
                old_value,
                new_value,
                change_amount,
                detected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scrape_run_id,
            change["url"],
            change["title"],
            "AVAILABILITY",
            change["old_status"],
            change["new_status"],
            None,
            detected_at,
        ))

    # --------------------------------------------------------
    # REMOVED LISTINGS
    # --------------------------------------------------------

    for change in changes["removed_listings"]:

        cursor.execute("""
            INSERT INTO change_events (
                scrape_run_id,
                property_url,
                title,
                change_type,
                old_value,
                new_value,
                change_amount,
                detected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scrape_run_id,
            change["url"],
            change["title"],
            "REMOVED_LISTING",
            change["availability"],
            None,
            None,
            detected_at,
        ))

    connection.commit()
    connection.close()