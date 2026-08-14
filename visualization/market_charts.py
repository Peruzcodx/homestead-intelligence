import sqlite3

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
DB_PATH = "database/estatepulse.db"


# ============================================================
# DATABASE
# ============================================================

def get_properties():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            price,
            neighborhood,
            property_type,
            availability,
            sqft
        FROM properties
    """)

    properties = cursor.fetchall()

    connection.close()

    return properties


# ============================================================
# PROPERTY TYPE DISTRIBUTION
# ============================================================

def property_type_distribution(properties):

    data = {}

    for property in properties:

        property_type = property[2]

        if property_type:
            data[property_type] = (
                data.get(property_type, 0) + 1
            )

    return data


# ============================================================
# AVAILABILITY DISTRIBUTION
# ============================================================

def availability_distribution(properties):

    data = {}

    for property in properties:

        availability = property[3]

        if availability:
            data[availability] = (
                data.get(availability, 0) + 1
            )

    return data


# ============================================================
# PRICE BY PROPERTY TYPE
# ============================================================

def average_price_by_property_type(properties):

    data = {}

    for property in properties:

        price = property[0]
        property_type = property[2]

        if price is None or not property_type:
            continue

        if property_type not in data:
            data[property_type] = []

        data[property_type].append(price)

    results = {}

    for property_type, prices in data.items():

        results[property_type] = (
            sum(prices) / len(prices)
        )

    return results


# ============================================================
# PRICE BY NEIGHBORHOOD
# ============================================================

def average_price_by_neighborhood(properties):

    data = {}

    for property in properties:

        price = property[0]
        neighborhood = property[1]

        if price is None or not neighborhood:
            continue

        if neighborhood not in data:
            data[neighborhood] = []

        data[neighborhood].append(price)

    results = {}

    for neighborhood, prices in data.items():

        results[neighborhood] = (
            sum(prices) / len(prices)
        )

    return results


# ============================================================
# PRICE SEGMENTS
# ============================================================

def price_segments(properties):

    segments = {
        "Under $500K": 0,
        "$500K - $999K": 0,
        "$1M - $1.49M": 0,
        "$1.5M - $2.49M": 0,
        "$2.5M+": 0,
    }

    for property in properties:

        price = property[0]

        if price is None:
            continue

        if price < 500_000:
            segments["Under $500K"] += 1

        elif price < 1_000_000:
            segments["$500K - $999K"] += 1

        elif price < 1_500_000:
            segments["$1M - $1.49M"] += 1

        elif price < 2_500_000:
            segments["$1.5M - $2.49M"] += 1

        else:
            segments["$2.5M+"] += 1

    return segments


# ============================================================
# PRICE PER SQFT BY NEIGHBORHOOD
# ============================================================

def price_per_sqft_by_neighborhood(properties):

    data = {}

    for property in properties:

        price = property[0]
        neighborhood = property[1]
        sqft = property[4]

        if (
            price is None
            or not neighborhood
            or sqft is None
            or sqft <= 0
        ):
            continue

        if neighborhood not in data:
            data[neighborhood] = []

        data[neighborhood].append(
            price / sqft
        )

    results = {}

    for neighborhood, values in data.items():

        results[neighborhood] = (
            sum(values) / len(values)
        )

    return results


# ============================================================
# CHART 1 — PROPERTY TYPE
# ============================================================

def plot_property_types(data):

    labels = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(8, 6))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.45}
    )

    plt.title("Property Type Distribution")

    plt.tight_layout()

    plt.savefig(
        "visualization/charts/property_type_distribution.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

# ============================================================
# CHART 2 — AVAILABILITY
# ============================================================

def plot_availability(data):

    labels = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(8, 6))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.45}
    )

    plt.title("Property Availability")

    plt.tight_layout()

    plt.savefig(
        "visualization/charts/availability_distribution.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()
# ============================================================
# CHART 3 — PRICE BY PROPERTY TYPE
# ============================================================
def plot_price_by_property_type(data):

    sorted_data = dict(
        sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    labels = list(sorted_data.keys())
    values = list(sorted_data.values())

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        labels,
        values
    )

    plt.title("Average Price by Property Type")
    plt.xlabel("Property Type")
    plt.ylabel("Average Price ($)")

    plt.gca().yaxis.set_major_formatter(
        mticker.StrMethodFormatter("${x:,.0f}")
    )

    plt.xticks(
        rotation=20
    )

    for bar, value in zip(bars, values):

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"${value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()

    plt.savefig(
        "visualization/charts/price_by_property_type.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

# ============================================================
# CHART 4 — PRICE BY NEIGHBORHOOD
# ============================================================
def plot_price_by_neighborhood(data):

    sorted_data = dict(
        sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    labels = list(sorted_data.keys())
    values = list(sorted_data.values())

    plt.figure(figsize=(10, 7))

    bars = plt.barh(
        labels,
        values
    )

    plt.title("Average Price by Neighborhood")
    plt.xlabel("Average Price ($)")
    plt.ylabel("Neighborhood")

    # Highest price at the top
    plt.gca().invert_yaxis()

    # Dollar formatting on X-axis
    plt.gca().xaxis.set_major_formatter(
        mticker.StrMethodFormatter("${x:,.0f}")
    )

    # Add values beside each bar
    for bar, value in zip(bars, values):

        plt.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"  ${value:,.0f}",
            va="center",
            fontsize=9
        )

    plt.tight_layout()

    plt.savefig(
        "visualization/charts/price_by_neighborhood.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()
# ============================================================
# CHART 5 — PRICE SEGMENTS
# ============================================================
def plot_price_segments(data):

    labels = list(data.keys())
    values = list(data.values())

    total = sum(values)

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        labels,
        values
    )

    plt.title("Property Distribution by Price Segment")
    plt.xlabel("Price Segment")
    plt.ylabel("Number of Properties")

    plt.xticks(rotation=15)

    # Add count and percentage above each bar
    for bar, value in zip(bars, values):

        percentage = (value / total) * 100

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value} ({percentage:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()

    plt.savefig(
        "visualization/charts/price_segments.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()
# ============================================================
# CHART 6 — PRICE PER SQFT BY NEIGHBORHOOD
# ============================================================
def plot_price_per_sqft(data):

    sorted_data = dict(
        sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    labels = list(sorted_data.keys())
    values = list(sorted_data.values())

    plt.figure(figsize=(10, 7))

    bars = plt.barh(
        labels,
        values
    )

    plt.title("Average Price per Sqft by Neighborhood")
    plt.xlabel("Average Price per Sqft ($)")
    plt.ylabel("Neighborhood")

    # Highest value at the top
    plt.gca().invert_yaxis()

    # Dollar formatting
    plt.gca().xaxis.set_major_formatter(
        mticker.StrMethodFormatter("${x:,.0f}")
    )

    # Add values beside each bar
    for bar, value in zip(bars, values):

        plt.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"  ${value:,.0f}/sqft",
            va="center",
            fontsize=9
        )

    plt.tight_layout()

    plt.savefig(
        "visualization/charts/price_per_sqft_by_neighborhood.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()
    # ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    properties = get_properties()

    print(
        f"Loaded {len(properties)} properties."
    )

    property_types = property_type_distribution(
        properties
    )

    availability = availability_distribution(
        properties
    )

    price_by_type = average_price_by_property_type(
        properties
    )

    price_by_area = average_price_by_neighborhood(
        properties
    )

    segments = price_segments(
        properties
    )

    price_sqft = price_per_sqft_by_neighborhood(
        properties
    )

    print("\n========== VISUALIZATION DATA ==========")

    print("\nProperty Types:")
    print(property_types)

    print("\nAvailability:")
    print(availability)

    print("\nAverage Price by Property Type:")
    print(price_by_type)

    print("\nAverage Price by Neighborhood:")
    print(price_by_area)

    print("\nPrice Segments:")
    print(segments)

    print("\nPrice/Sqft by Neighborhood:")
    print(price_sqft)

    print("\n========== CREATING CHARTS ==========")

    plot_property_types(property_types)

    plot_availability(availability)

    plot_price_by_property_type(price_by_type)

    plot_price_by_neighborhood(price_by_area)

    plot_price_segments(segments)

    plot_price_per_sqft(price_sqft)

    print("\n========== VISUALIZATION COMPLETE ==========")