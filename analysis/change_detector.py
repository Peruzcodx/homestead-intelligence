import sqlite3


DB_PATH = "database/estatepulse.db"


# ============================================================
# GET SCRAPE RUNS
# ============================================================

def get_scrape_runs():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            scrape_run_id,
            MAX(scraped_at) AS scraped_at
        FROM property_snapshots
        WHERE scrape_run_id IS NOT NULL
        GROUP BY scrape_run_id
        ORDER BY scrape_run_id DESC
    """)

    runs = cursor.fetchall()

    connection.close()

    return runs


# ============================================================
# GET SNAPSHOT FOR A SCRAPE RUN
# ============================================================

def get_snapshot(scrape_run_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            property_url,
            title,
            price,
            availability
        FROM property_snapshots
        WHERE rowid IN (
            SELECT MAX(rowid)
            FROM property_snapshots
            WHERE scrape_run_id = ?
            GROUP BY property_url
        )
    """, (scrape_run_id,))

    rows = cursor.fetchall()

    connection.close()

    return {
        row[0]: {
            "title": row[1],
            "price": row[2],
            "availability": row[3],
        }
        for row in rows
    }


# ============================================================
# GET CHANGE HISTORY
# ============================================================

def get_change_history():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            detected_at,
            change_type,
            title,
            old_value,
            new_value,
            change_amount,
            property_url
        FROM change_events
        ORDER BY detected_at DESC, id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "detected_at": row[0],
            "change_type": row[1],
            "title": row[2],
            "old_value": row[3],
            "new_value": row[4],
            "change_amount": row[5],
            "url": row[6],
        }
        for row in rows
    ]


# ============================================================
# DETECT CHANGES
# ============================================================

def detect_changes():

    scrape_runs = get_scrape_runs()

    if len(scrape_runs) < 2:

        return {
            "new_listings": [],
            "price_changes": [],
            "availability_changes": [],
            "removed_listings": [],
            "latest_scrape": (
                scrape_runs[0][0]
                if scrape_runs
                else None
            ),
            "previous_scrape": None,
        }

    latest_run = scrape_runs[0][0]
    previous_run = scrape_runs[1][0]

    latest = get_snapshot(latest_run)
    previous = get_snapshot(previous_run)

    new_listings = []
    price_changes = []
    availability_changes = []
    removed_listings = []

    # ========================================================
    # NEW / CHANGED PROPERTIES
    # ========================================================

    for url, current in latest.items():

        if url not in previous:

            new_listings.append({
                "url": url,
                "title": current["title"],
                "price": current["price"],
                "availability": current["availability"],
            })

            continue

        old = previous[url]

        # ----------------------------------------------------
        # PRICE CHANGE
        # ----------------------------------------------------

        if (
            old["price"] is not None
            and current["price"] is not None
            and old["price"] != current["price"]
        ):

            price_changes.append({
                "url": url,
                "title": current["title"],
                "old_price": old["price"],
                "new_price": current["price"],
                "change": (
                    current["price"]
                    - old["price"]
                ),
            })

        # ----------------------------------------------------
        # AVAILABILITY CHANGE
        # ----------------------------------------------------

        if old["availability"] != current["availability"]:

            availability_changes.append({
                "url": url,
                "title": current["title"],
                "old_status": old["availability"],
                "new_status": current["availability"],
            })

    # ========================================================
    # REMOVED PROPERTIES
    # ========================================================

    for url, old in previous.items():

        if url not in latest:

            removed_listings.append({
                "url": url,
                "title": old["title"],
                "price": old["price"],
                "availability": old["availability"],
            })

    return {
        "new_listings": new_listings,
        "price_changes": price_changes,
        "availability_changes": availability_changes,
        "removed_listings": removed_listings,
        "latest_scrape": latest_run,
        "previous_scrape": previous_run,
    }


# ============================================================
# TEST CHANGE HISTORY
# ============================================================

if __name__ == "__main__":

    history = get_change_history()

    for change in history:
        print(change)
