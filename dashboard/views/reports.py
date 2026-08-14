import streamlit as st
import plotly.express as px
import pandas as pd

from analysis.market_analysis import (
    get_properties,
    analyze_price_statistics,
    analyze_price_per_sqft_statistics,
    analyze_availability,
    analyze_price_segments,
    analyze_area_intelligence,
    analyze_price_by_property_type,
)

from analysis.market_insights import (
    generate_pricing_insight,
    generate_location_insight,
    generate_inventory_insight,
    generate_market_movement_insight,
)


def render_reports():

    st.title("Market Intelligence Report")

    st.markdown(
        """
        <div class="section-description">
            Summary of current market conditions based on the
            latest property data.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD MARKET DATA
    # ========================================================

    properties = get_properties()

    if not properties:
        st.warning(
            "No property data is available for this report."
        )
        return

    # ========================================================
    # MARKET STATISTICS
    # ========================================================

    price_stats = analyze_price_statistics(
        properties
    )

    sqft_stats = analyze_price_per_sqft_statistics(
        properties
    )

    availability = analyze_availability(
        properties
    )

    active_listings = availability.get(
        "ACTIVE",
        0,
    )

    # ========================================================
    # MARKET SNAPSHOT
    # ========================================================

    st.markdown(
        '<div class="section-title">Market Snapshot</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Listings",
            f"{len(properties):,}",
        )

    with col2:
        st.metric(
            "Average Price",
            f"${price_stats['average']:,.0f}",
        )

    with col3:
        st.metric(
            "Median Price",
            f"${price_stats['median']:,.0f}",
        )

    with col4:
        st.metric(
            "Average $/Sqft",
            f"${sqft_stats['average']:,.0f}",
        )

    with col5:
        st.metric(
            "Active Listings",
            f"{active_listings:,}",
        )

    # ========================================================
    # KEY MARKET INSIGHTS
    # ========================================================

    pricing_insight = generate_pricing_insight()
    location_insight = generate_location_insight()
    inventory_insight = generate_inventory_insight()
    movement_insight = generate_market_movement_insight()

    st.markdown(
        '<div class="section-title">Key Market Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Automated intelligence derived from current pricing,
            location, inventory, and market movement data.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("#### Pricing Insight")

        st.write(
            f"**{pricing_insight['dominant_segment']}** is the "
            f"dominant price segment, accounting for "
            f"**{pricing_insight['percentage']:.1f}%** "
            f"of current listings."
        )

    with col2:

        st.markdown("#### Location Insight")

        st.write(
            f"**{location_insight['highest_average_price_area']}** "
            f"has the highest average listing price at "
            f"**${location_insight['highest_average_price']:,.0f}**."
        )

        st.write(
            f"It also leads in total listed market value at "
            f"**${location_insight['highest_total_market_value']:,.0f}**."
        )

    with col3:

        st.markdown("#### Inventory Insight")

        st.write(
            f"**{inventory_insight['dominant_status']}** listings "
            f"represent **{inventory_insight['dominant_percentage']:.1f}%** "
            f"of the current market."
        )

    # ========================================================
    # MARKET MOVEMENT
    # ========================================================

    st.markdown(
        '<div class="section-title">Market Movement</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Changes detected between the two latest scrape runs.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if movement_insight["has_movement"]:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "New Listings",
                movement_insight["new_listings"],
            )

        with col2:
            st.metric(
                "Price Changes",
                movement_insight["price_changes"],
            )

        with col3:
            st.metric(
                "Availability Changes",
                movement_insight["availability_changes"],
            )

        with col4:
            st.metric(
                "Removed Listings",
                movement_insight["removed_listings"],
            )

    else:

        st.info(
            "No measurable market movement was detected "
            "between the two latest scrape runs."
        )

    # ========================================================
    # PRICING OVERVIEW
    # ========================================================

    st.markdown(
        '<div class="section-title">Pricing Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Current pricing distribution and average prices
            across property types.
        </div>
        """,
        unsafe_allow_html=True,
    )

    price_segments = analyze_price_segments(
        properties
    )

    price_segment_df = pd.DataFrame(
        list(price_segments.items()),
        columns=[
            "Price Range",
            "Listings",
        ],
    )

    price_segment_df["Market Share"] = (
        price_segment_df["Listings"]
        / len(properties)
        * 100
    )

    col1, col2 = st.columns(2)

    # ========================================================
    # PRICE DISTRIBUTION
    # ========================================================

    with col1:

        st.markdown("#### Price Distribution")

        fig = px.bar(
            price_segment_df,
            x="Price Range",
            y="Listings",
            labels={
                "Price Range": "Price Range",
                "Listings": "Listings",
            },
        )

        fig.update_layout(
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"staticPlot": True},
        )

    # ========================================================
    # AVERAGE PRICE BY PROPERTY TYPE
    # ========================================================

    with col2:

        price_by_type = analyze_price_by_property_type(
            properties
        )

        property_type_df = pd.DataFrame.from_dict(
            price_by_type,
            orient="index",
        )

        property_type_df = (
            property_type_df
            .reset_index()
            .rename(
                columns={
                    "index": "Property Type",
                    "average_price": "Average Price",
                    "count": "Listings",
                }
            )
            .sort_values(
                "Average Price",
                ascending=False,
            )
        )

        st.markdown(
            "#### Average Price by Property Type"
        )

        fig = px.bar(
            property_type_df,
            x="Property Type",
            y="Average Price",
            labels={
                "Property Type": "Property Type",
                "Average Price": "Average Price",
            },
        )

        fig.update_layout(
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"staticPlot": True},
        )

    # ========================================================
    # NEIGHBORHOOD INTELLIGENCE
    # ========================================================

    st.markdown(
        '<div class="section-title">Neighborhood Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Comparative view of pricing, inventory, and market
            value across neighborhoods.
        </div>
        """,
        unsafe_allow_html=True,
    )

    area_intelligence = analyze_area_intelligence(
        properties
    )

    neighborhood_df = pd.DataFrame.from_dict(
        area_intelligence,
        orient="index",
    )

    neighborhood_df = (
        neighborhood_df
        .reset_index()
        .rename(
            columns={
                "index": "Neighborhood",
                "listings": "Listings",
                "average_price": "Average Price",
                "median_price": "Median Price",
                "weighted_price_per_sqft": "$/Sqft",
                "total_market_value": "Total Market Value",
            }
        )
    )

    neighborhood_df = neighborhood_df[
        [
            "Neighborhood",
            "Listings",
            "Average Price",
            "Median Price",
            "$/Sqft",
            "Total Market Value",
        ]
    ]

    neighborhood_df = neighborhood_df.sort_values(
        "Average Price",
        ascending=False,
    )

    # ========================================================
    # KEY MARKET TAKEAWAY
    # ========================================================

    st.markdown(
        '<div class="section-title">Market Takeaway</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Automated interpretation of the current market conditions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    takeaway = (
        f"The market is currently concentrated in the "
        f"{pricing_insight['dominant_segment']} price range, "
        f"representing {pricing_insight['percentage']:.1f}% "
        f"of current listings. "
        f"{location_insight['highest_average_price_area']} "
        f"has the highest average listing price at "
        f"${location_insight['highest_average_price']:,.0f} "
        f"and the highest total listed market value at "
        f"${location_insight['highest_total_market_value']:,.0f}. "
        f"Active listings account for "
        f"{inventory_insight['dominant_percentage']:.1f}% "
        f"of tracked inventory."
    )

    if movement_insight["has_movement"]:

        takeaway += (
            f" The latest scrape comparison detected "
            f"{movement_insight['new_listings']} new listings, "
            f"{movement_insight['price_changes']} price changes, "
            f"{movement_insight['availability_changes']} "
            f"availability changes, and "
            f"{movement_insight['removed_listings']} removed listings."
        )

    else:

        takeaway += (
            " No measurable market movement was detected "
            "between the two latest scrape runs."
        )

    st.info(takeaway)

    # ========================================================
    # NEIGHBORHOOD DATA TABLE
    # ========================================================

    st.dataframe(
        neighborhood_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Neighborhood": st.column_config.TextColumn(
                "Neighborhood",
                width="medium",
            ),
            "Listings": st.column_config.NumberColumn(
                "Listings",
                format="%d",
            ),
            "Average Price": st.column_config.NumberColumn(
                "Average Price",
                format="$%,.0f",
            ),
            "Median Price": st.column_config.NumberColumn(
                "Median Price",
                format="$%,.0f",
            ),
            "$/Sqft": st.column_config.NumberColumn(
                "$/Sqft",
                format="$%,.0f",
            ),
            "Total Market Value": st.column_config.NumberColumn(
                "Total Market Value",
                format="$%,.0f",
            ),
        },
    )