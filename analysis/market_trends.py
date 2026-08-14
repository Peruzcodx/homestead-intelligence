import sqlite3


DB_PATH = "database/estatepulse.db"


# ============================================================
# GET MARKET SNAPSHOTS
# ============================================================

def get_market_snapshots():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            scrape_run_id,
            MAX(scraped_at) AS scraped_at,
            COUNT(*) AS total_properties,
            AVG(price) AS average_price
        FROM property_snapshots
        WHERE
            scrape_run_id IS NOT NULL
            AND price IS NOT NULL
        GROUP BY scrape_run_id
        ORDER BY scrape_run_id
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# GET AVAILABILITY TRENDS
# ============================================================

def get_availability_trends():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            scrape_run_id,
            availability,
            COUNT(*) AS property_count
        FROM property_snapshots
        WHERE
            scrape_run_id IS NOT NULL
            AND availability IS NOT NULL
        GROUP BY scrape_run_id, availability
        ORDER BY scrape_run_id, availability
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# MARKET TREND SUMMARY
# ============================================================

def get_market_trend_summary():

    snapshots = get_market_snapshots()

    if not snapshots:
        return None

    first_snapshot = snapshots[0]
    latest_snapshot = snapshots[-1]

    first_average_price = first_snapshot[3]
    latest_average_price = latest_snapshot[3]

    if (
        first_average_price is not None
        and first_average_price != 0
    ):

        price_change = (
            latest_average_price
            - first_average_price
        )

        price_change_percent = (
            price_change
            / first_average_price
        ) * 100

    else:

        price_change = 0
        price_change_percent = 0

    return {
        "first_run": first_snapshot[0],
        "latest_run": latest_snapshot[0],

        "first_date": first_snapshot[1],
        "latest_date": latest_snapshot[1],

        "first_average_price": first_average_price,
        "latest_average_price": latest_average_price,

        "price_change": price_change,
        "price_change_percent": price_change_percent,

        "first_property_count": first_snapshot[2],
        "latest_property_count": latest_snapshot[2],
    }