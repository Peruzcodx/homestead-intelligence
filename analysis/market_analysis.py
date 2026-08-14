import sqlite3


from statistics import median
DB_PATH = "database/estatepulse.db"


# ============================================================
# DATABASE
# ============================================================

def get_properties():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
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
        FROM properties
    """)

    properties = cursor.fetchall()

    connection.close()

    return properties


# ============================================================
# BASIC PRICE ANALYSIS
# ============================================================

def analyze_prices(properties):

    prices = [
        property[3]
        for property in properties
        if property[3] is not None
    ]

    if not prices:
        return None

    return {
        "average": sum(prices) / len(prices),
        "highest": max(prices),
        "lowest": min(prices),
    }

def analyze_price_statistics(properties):

    prices = [
        property[3]
        for property in properties
        if property[3] is not None
    ]

    if not prices:
        return None

    return {
        "average": sum(prices) / len(prices),
        "median": median(prices),
        "highest": max(prices),
        "lowest": min(prices),
    }


def analyze_price_per_sqft_statistics(properties):

    price_per_sqft = []

    total_price = 0
    total_sqft = 0

    for property in properties:

        price = property[3]
        sqft = property[11]

        if price is not None and sqft and sqft > 0:

            price_per_sqft.append(price / sqft)

            total_price += price
            total_sqft += sqft

    if not price_per_sqft:
        return None

    weighted_price_per_sqft = (
        total_price / total_sqft
        if total_sqft > 0
        else None
    )

    return {
        "average": sum(price_per_sqft) / len(price_per_sqft),
        "median": median(price_per_sqft),
        "highest": max(price_per_sqft),
        "lowest": min(price_per_sqft),
        "weighted": weighted_price_per_sqft,
    }
# ============================================================
# PRICE PER SQFT
# ============================================================

def analyze_price_per_sqft(properties):

    values = []

    for property in properties:

        price = property[3]
        sqft = property[11]

        if price is not None and sqft and sqft > 0:
            values.append(price / sqft)

    if not values:
        return None

    return {
        "average": sum(values) / len(values),
        "highest": max(values),
        "lowest": min(values),
    }


# ============================================================
# AVERAGE PRICE BY PROPERTY TYPE
# ============================================================

def analyze_price_by_property_type(properties):

    data = {}

    for property in properties:

        property_type = property[12]
        price = property[3]

        if property_type and price is not None:

            if property_type not in data:
                data[property_type] = []

            data[property_type].append(price)

    results = {}

    for property_type, prices in data.items():

        results[property_type] = {
            "count": len(prices),
            "average_price": sum(prices) / len(prices),
            "highest_price": max(prices),
            "lowest_price": min(prices),
        }

    return results


# ============================================================
# AVERAGE PRICE BY NEIGHBORHOOD
# ============================================================

def analyze_price_by_neighborhood(properties):

    data = {}

    for property in properties:

        neighborhood = property[8]
        price = property[3]

        if neighborhood and price is not None:

            if neighborhood not in data:
                data[neighborhood] = []

            data[neighborhood].append(price)

    results = {}

    for neighborhood, prices in data.items():

        results[neighborhood] = {
            "count": len(prices),
            "average_price": sum(prices) / len(prices),
            "highest_price": max(prices),
            "lowest_price": min(prices),
        }

    return results


# ============================================================
# AVERAGE PRICE BY BEDROOM COUNT
# ============================================================

def analyze_price_by_bedrooms(properties):

    data = {}

    for property in properties:

        bedrooms = property[9]
        price = property[3]

        if bedrooms is not None and price is not None:

            if bedrooms not in data:
                data[bedrooms] = []

            data[bedrooms].append(price)

    results = {}

    for bedrooms, prices in data.items():

        results[bedrooms] = {
            "count": len(prices),
            "average_price": sum(prices) / len(prices),
        }

    return results


# ============================================================
# INVENTORY BY AVAILABILITY
# ============================================================

def analyze_availability(properties):

    availability = {}

    for property in properties:

        status = property[13]

        if status:

            availability[status] = (
                availability.get(status, 0) + 1
            )

    return availability


# ============================================================
# AVERAGE SQFT BY PROPERTY TYPE
# ============================================================

def analyze_sqft_by_property_type(properties):

    data = {}

    for property in properties:

        property_type = property[12]
        sqft = property[11]

        if property_type and sqft is not None:

            if property_type not in data:
                data[property_type] = []

            data[property_type].append(sqft)

    results = {}

    for property_type, sqft_values in data.items():

        results[property_type] = {
            "count": len(sqft_values),
            "average_sqft": sum(sqft_values) / len(sqft_values),
            "largest_sqft": max(sqft_values),
            "smallest_sqft": min(sqft_values),
        }

    return results


# ============================================================
# MARKET VALUE BY AREA
# ============================================================

def analyze_market_value_by_area(properties):

    data = {}

    for property in properties:

        neighborhood = property[8]
        price = property[3]

        if neighborhood and price is not None:

            if neighborhood not in data:
                data[neighborhood] = []

            data[neighborhood].append(price)

    results = {}

    for neighborhood, prices in data.items():

        results[neighborhood] = {
            "property_count": len(prices),
            "total_market_value": sum(prices),
            "average_value": sum(prices) / len(prices),
        }

    return results


# ============================================================
# PROPERTY TYPE DISTRIBUTION
# ============================================================

def analyze_property_types(properties):

    property_types = {}

    for property in properties:

        property_type = property[12]

        if property_type:

            property_types[property_type] = (
                property_types.get(property_type, 0) + 1
            )

    return property_types
def analyze_price_segments(properties):

    segments = {
        "Under $500K": 0,
        "$500K - $999K": 0,
        "$1M - $1.49M": 0,
        "$1.5M - $2.49M": 0,
        "$2.5M+": 0,
    }

    for property in properties:

        price = property[3]

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


def analyze_area_intelligence(properties):

    areas = {}

    for property in properties:

        neighborhood = property[8]
        price = property[3]
        sqft = property[11]

        if not neighborhood:
            continue

        if neighborhood not in areas:
            areas[neighborhood] = {
                "prices": [],
                "sqft": [],
            }

        if price is not None:
            areas[neighborhood]["prices"].append(price)

        if sqft is not None and sqft > 0:
            areas[neighborhood]["sqft"].append(sqft)

    results = {}

    for neighborhood, data in areas.items():

        prices = data["prices"]
        sqft_values = data["sqft"]

        if not prices:
            continue

        total_value = sum(prices)

        average_price = total_value / len(prices)

        median_price = median(prices)

        if sqft_values:
            average_sqft = sum(sqft_values) / len(sqft_values)
        else:
            average_sqft = None

        total_sqft = sum(sqft_values)

        if total_sqft > 0:
            weighted_price_per_sqft = (
                total_value / total_sqft
            )
        else:
            weighted_price_per_sqft = None

        results[neighborhood] = {
            "listings": len(prices),
            "average_price": average_price,
            "median_price": median_price,
            "total_market_value": total_value,
            "average_sqft": average_sqft,
            "weighted_price_per_sqft": weighted_price_per_sqft,
        }

    return results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    properties = get_properties()

    print("\n========== MARKET INTELLIGENCE ==========")

    print(f"Total properties: {len(properties)}")


    # --------------------------------------------------------
    # PRICE
    # --------------------------------------------------------

    price_analysis = analyze_price_statistics(properties)
    print("\n========== PRICE STATISTICS ==========")

    print(f"Average price: ${price_analysis['average']:,.2f}")
    print(f"Median price: ${price_analysis['median']:,.2f}")
    print(f"Highest price: ${price_analysis['highest']:,.2f}")
    print(f"Lowest price: ${price_analysis['lowest']:,.2f}")

    # --------------------------------------------------------
    # PRICE PER SQFT
    # --------------------------------------------------------

    price_per_sqft = analyze_price_per_sqft_statistics(properties)

    print("\n========== PRICE PER SQFT ==========")

    print(
        f"Average: ${price_per_sqft['average']:,.2f}/sqft"
    )

    print(
        f"Median: ${price_per_sqft['median']:,.2f}/sqft"
    )

    print(
        f"Weighted: ${price_per_sqft['weighted']:,.2f}/sqft"
    )

    print(
        f"Highest: ${price_per_sqft['highest']:,.2f}/sqft"
    )

    print(
        f"Lowest: ${price_per_sqft['lowest']:,.2f}/sqft"
    )
    # --------------------------------------------------------
    # PROPERTY TYPES
    # --------------------------------------------------------

    print("\n========== PROPERTY TYPES ==========")

    property_types = analyze_property_types(properties)

    for property_type, count in sorted(
        property_types.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{property_type}: {count}")


    # --------------------------------------------------------
    # PRICE BY PROPERTY TYPE
    # --------------------------------------------------------

    print("\n========== PRICE BY PROPERTY TYPE ==========")

    price_by_type = analyze_price_by_property_type(properties)

    for property_type, data in sorted(
        price_by_type.items(),
        key=lambda item: item[1]["average_price"],
        reverse=True
    ):

        print(
            f"{property_type}: "
            f"{data['count']} properties | "
            f"Average: ${data['average_price']:,.2f} | "
            f"Highest: ${data['highest_price']:,.2f} | "
            f"Lowest: ${data['lowest_price']:,.2f}"
        )


    # --------------------------------------------------------
    # PRICE BY NEIGHBORHOOD
    # --------------------------------------------------------

    print("\n========== PRICE BY NEIGHBORHOOD ==========")

    price_by_neighborhood = analyze_price_by_neighborhood(
        properties
    )

    for neighborhood, data in sorted(
        price_by_neighborhood.items(),
        key=lambda item: item[1]["average_price"],
        reverse=True
    ):

        print(
            f"{neighborhood}: "
            f"{data['count']} properties | "
            f"Average: ${data['average_price']:,.2f}"
        )


    # --------------------------------------------------------
    # PRICE BY BEDROOMS
    # --------------------------------------------------------

    print("\n========== PRICE BY BEDROOMS ==========")

    price_by_bedrooms = analyze_price_by_bedrooms(properties)

    for bedrooms, data in sorted(
        price_by_bedrooms.items()
    ):

        label = "Studio" if bedrooms == 0 else f"{bedrooms} bedroom"

        if bedrooms != 1:
            label += "s" if bedrooms != 0 else ""

        print(
            f"{label}: "
            f"{data['count']} properties | "
            f"Average: ${data['average_price']:,.2f}"
        )

    print("\n========== PRICE SEGMENTS ==========")

    price_segments = analyze_price_segments(properties)

    total_properties = len(properties)

    for segment, count in price_segments.items():

        percentage = (
            count / total_properties * 100
            if total_properties > 0
            else 0
        )

        print(
            f"{segment}: "
            f"{count} properties "
            f"({percentage:.1f}%)"
        )

    # --------------------------------------------------------
    # AVAILABILITY
    # --------------------------------------------------------

    print("\n========== AVAILABILITY ==========")

    availability = analyze_availability(properties)

    for status, count in sorted(
        availability.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        print(f"{status}: {count}")


    # --------------------------------------------------------
    # SQFT BY PROPERTY TYPE
    # --------------------------------------------------------

    print("\n========== SQFT BY PROPERTY TYPE ==========")

    sqft_by_type = analyze_sqft_by_property_type(properties)

    for property_type, data in sorted(
        sqft_by_type.items(),
        key=lambda item: item[1]["average_sqft"],
        reverse=True
    ):

        print(
            f"{property_type}: "
            f"Average {data['average_sqft']:,.0f} sqft | "
            f"Largest {data['largest_sqft']:,} sqft | "
            f"Smallest {data['smallest_sqft']:,} sqft"
        )


    # --------------------------------------------------------
    # MARKET VALUE BY AREA
    # --------------------------------------------------------

    print("\n========== MARKET VALUE BY AREA ==========")

    market_value = analyze_market_value_by_area(properties)

    for neighborhood, data in sorted(
        market_value.items(),
        key=lambda item: item[1]["total_market_value"],
        reverse=True
    ):

        print(
            f"{neighborhood}: "
            f"{data['property_count']} properties | "
            f"Total Value: ${data['total_market_value']:,.2f} | "
            f"Average: ${data['average_value']:,.2f}"
        )

    print("\n========== AREA INTELLIGENCE ==========")

    area_intelligence = analyze_area_intelligence(properties)

    for neighborhood, data in sorted(
        area_intelligence.items(),
        key=lambda item: item[1]["average_price"],
        reverse=True
    ):

        sqft = (
            f"{data['average_sqft']:,.0f}"
            if data["average_sqft"] is not None
            else "N/A"
        )

        price_per_sqft = (
            f"${data['weighted_price_per_sqft']:,.2f}"
            if data["weighted_price_per_sqft"] is not None
            else "N/A"
        )

        print(
            f"{neighborhood}: "
            f"{data['listings']} listings | "
            f"Average: ${data['average_price']:,.2f} | "
            f"Median: ${data['median_price']:,.2f} | "
            f"$/{'sqft'}: {price_per_sqft} | "
            f"Avg Size: {sqft} sqft | "
            f"Market Value: ${data['total_market_value']:,.2f}"
        )


    print("\n========== ANALYSIS COMPLETE ==========")