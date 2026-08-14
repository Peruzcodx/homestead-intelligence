from analysis.market_analysis import (
    get_properties,
    analyze_prices,
    analyze_price_statistics,
    analyze_price_per_sqft_statistics,
    analyze_price_per_sqft,
    analyze_price_by_property_type,
    analyze_price_by_neighborhood,
    analyze_price_by_bedrooms,
    analyze_availability,
    analyze_sqft_by_property_type,
    analyze_market_value_by_area,
    analyze_property_types,
    analyze_price_segments,
    analyze_area_intelligence,
)

from analysis.change_detector import detect_changes
from analysis.market_trends import get_market_trend_summary


# ============================================================
# MARKET REPORT
# ============================================================

def generate_market_report():

    properties = get_properties()

    return {
        "total_properties": len(properties),

        "prices": analyze_prices(properties),

        "price_statistics":
            analyze_price_statistics(properties),

        "price_per_sqft_statistics":
            analyze_price_per_sqft_statistics(properties),

        "price_per_sqft":
            analyze_price_per_sqft(properties),

        "price_by_property_type":
            analyze_price_by_property_type(properties),

        "price_by_neighborhood":
            analyze_price_by_neighborhood(properties),

        "price_by_bedrooms":
            analyze_price_by_bedrooms(properties),

        "availability":
            analyze_availability(properties),

        "sqft_by_property_type":
            analyze_sqft_by_property_type(properties),

        "market_value_by_area":
            analyze_market_value_by_area(properties),

        "property_types":
            analyze_property_types(properties),

        "price_segments":
            analyze_price_segments(properties),

        "area_intelligence":
            analyze_area_intelligence(properties),

        "changes":
            detect_changes(),

        "trends":
            get_market_trend_summary(),
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    report = generate_market_report()

    print("\n========== HOMESTEAD MARKET REPORT ==========")

    print("\nTotal Properties:")
    print(report["total_properties"])

    print("\nPrices:")
    print(report["prices"])

    print("\nPrice Statistics:")
    print(report["price_statistics"])

    print("\nPrice per Sqft Statistics:")
    print(report["price_per_sqft_statistics"])

    print("\nPrice by Property Type:")
    print(report["price_by_property_type"])

    print("\nPrice by Neighborhood:")
    print(report["price_by_neighborhood"])

    print("\nPrice by Bedrooms:")
    print(report["price_by_bedrooms"])

    print("\nAvailability:")
    print(report["availability"])

    print("\nProperty Types:")
    print(report["property_types"])

    print("\nPrice Segments:")
    print(report["price_segments"])

    print("\nChanges:")
    print(report["changes"])

    print("\nMarket Trends:")
    print(report["trends"])

    print("\n========== REPORT COMPLETE ==========")