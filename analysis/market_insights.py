from analysis.market_analysis import (
    get_properties,
    analyze_price_statistics,
    analyze_price_per_sqft_statistics,
    analyze_availability,
    analyze_price_segments,
)

def generate_market_summary():

    properties = get_properties()

    if not properties:
        return None

    price_stats = analyze_price_statistics(
        properties
    )

    sqft_stats = analyze_price_per_sqft_statistics(
        properties
    )

    availability = analyze_availability(
        properties
    )

    total_listings = len(properties)

    active_listings = availability.get(
        "ACTIVE",
        0,
    )

    active_percentage = (
        active_listings
        / total_listings
        * 100
        if total_listings > 0
        else 0
    )

    return {
        "total_listings": total_listings,
        "average_price": price_stats["average"],
        "median_price": price_stats["median"],
        "highest_price": price_stats["highest"],
        "lowest_price": price_stats["lowest"],
        "average_price_per_sqft": sqft_stats["average"],
        "active_listings": active_listings,
        "active_percentage": active_percentage,
    }

def generate_pricing_insight():

    properties = get_properties()

    if not properties:
        return None

    price_segments = analyze_price_segments(
        properties
    )

    total_listings = len(properties)

    if not price_segments or total_listings == 0:
        return None

    dominant_segment = max(
        price_segments,
        key=price_segments.get,
    )

    dominant_count = price_segments[
        dominant_segment
    ]

    dominant_percentage = (
        dominant_count
        / total_listings
        * 100
    )

    return {
        "dominant_segment": dominant_segment,
        "listing_count": dominant_count,
        "percentage": dominant_percentage,
        "segments": price_segments,
    }

def generate_location_insight():

    properties = get_properties()

    if not properties:
        return None

    from analysis.market_analysis import (
        analyze_price_by_neighborhood,
        analyze_market_value_by_area,
    )

    price_by_neighborhood = (
        analyze_price_by_neighborhood(properties)
    )

    market_value_by_area = (
        analyze_market_value_by_area(properties)
    )

    if not price_by_neighborhood:
        return None

    highest_average_area = max(
        price_by_neighborhood,
        key=lambda area: price_by_neighborhood[
            area
        ]["average_price"],
    )

    highest_average_data = (
        price_by_neighborhood[
            highest_average_area
        ]
    )

    highest_value_area = max(
        market_value_by_area,
        key=lambda area: market_value_by_area[
            area
        ]["total_market_value"],
    )

    highest_value_data = (
        market_value_by_area[
            highest_value_area
        ]
    )

    return {
        "highest_average_price_area": (
            highest_average_area
        ),
        "highest_average_price": (
            highest_average_data[
                "average_price"
            ]
        ),
        "highest_average_price_count": (
            highest_average_data[
                "count"
            ]
        ),
        "highest_value_area": (
            highest_value_area
        ),
        "highest_total_market_value": (
            highest_value_data[
                "total_market_value"
            ]
        ),
        "highest_value_listing_count": (
            highest_value_data[
                "property_count"
            ]
        ),
    }

def generate_inventory_insight():

    properties = get_properties()

    if not properties:
        return None

    availability = analyze_availability(
        properties
    )

    total_listings = len(properties)

    if not availability or total_listings == 0:
        return None

    dominant_status = max(
        availability,
        key=availability.get,
    )

    dominant_count = availability[
        dominant_status
    ]

    dominant_percentage = (
        dominant_count
        / total_listings
        * 100
    )

    return {
        "total_listings": total_listings,
        "availability": availability,
        "dominant_status": dominant_status,
        "dominant_count": dominant_count,
        "dominant_percentage": dominant_percentage,
    }

def generate_market_movement_insight():

    from analysis.change_detector import detect_changes

    changes = detect_changes()

    new_listings = changes["new_listings"]
    price_changes = changes["price_changes"]
    availability_changes = changes[
        "availability_changes"
    ]
    removed_listings = changes[
        "removed_listings"
    ]

    new_count = len(new_listings)
    price_change_count = len(price_changes)
    availability_change_count = len(
        availability_changes
    )
    removed_count = len(removed_listings)

    net_inventory_change = (
        new_count - removed_count
    )

    total_price_change = sum(
        change["change"]
        for change in price_changes
        if change["change"] is not None
    )

    has_movement = any([
        new_count > 0,
        price_change_count > 0,
        availability_change_count > 0,
        removed_count > 0,
    ])

    return {
        "latest_scrape": changes[
            "latest_scrape"
        ],
        "previous_scrape": changes[
            "previous_scrape"
        ],
        "new_listings": new_count,
        "price_changes": price_change_count,
        "availability_changes": (
            availability_change_count
        ),
        "removed_listings": removed_count,
        "net_inventory_change": (
            net_inventory_change
        ),
        "total_price_change": (
            total_price_change
        ),
        "has_movement": has_movement,
    }
