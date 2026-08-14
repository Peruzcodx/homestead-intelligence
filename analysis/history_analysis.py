import sqlite3


DB_PATH = "database/estatepulse.db"


# ============================================================
# GET PROPERTY HISTORY
# ============================================================

def get_property_history(property_url):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            price,
            availability,
            scraped_at
        FROM property_snapshots
        WHERE property_url = ?
        ORDER BY scraped_at ASC
        """,
        (property_url,)
    )

    history = cursor.fetchall()

    connection.close()

    return history


# ============================================================
# GET PROPERTY CHANGES
# ============================================================

def get_property_changes(property_url):

    history = get_property_history(property_url)

    if len(history) < 2:
        return None

    first_price = history[0][0]
    latest_price = history[-1][0]

    first_availability = history[0][1]
    latest_availability = history[-1][1]

    if first_price is not None and latest_price is not None:
        price_change = latest_price - first_price

        if first_price != 0:
            price_change_percent = (
                price_change / first_price
            ) * 100
        else:
            price_change_percent = 0

    else:
        price_change = None
        price_change_percent = None

    return {
        "first_seen": history[0][2],
        "last_seen": history[-1][2],
        "observations": len(history),
        "first_price": first_price,
        "latest_price": latest_price,
        "price_change": price_change,
        "price_change_percent": price_change_percent,
        "first_availability": first_availability,
        "latest_availability": latest_availability,
    }