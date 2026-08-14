import streamlit as st

import pandas as pd
import plotly.graph_objects as go
from analysis.market_analysis import (
    get_properties,
    analyze_price_statistics,
    analyze_price_per_sqft_statistics,
    analyze_price_by_property_type,
    analyze_market_value_by_area,
    analyze_area_intelligence,
    analyze_price_segments,
    analyze_availability,
)

from analysis.market_insights import (
    generate_market_summary,
    generate_pricing_insight,
    generate_location_insight,
    generate_inventory_insight,
    generate_market_movement_insight,
)

def render_analysis():

    # ========================================================
    # HEADER
    # ========================================================

    st.title("Market Analysis")

    st.markdown(
        """
        <div class="section-description">
            Analyze pricing, property types, neighborhoods,
            and market value across the current market.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    properties = get_properties()

    if not properties:
        st.warning(
            "No property data is available for analysis."
        )
        return

        # ========================================================
    # MARKET INTELLIGENCE
    # ========================================================

    market_summary = generate_market_summary()
    pricing_insight = generate_pricing_insight()
    location_insight = generate_location_insight()
    inventory_insight = generate_inventory_insight()
    movement_insight = generate_market_movement_insight()

    st.markdown(
        '<div class="section-title">Market Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Key signals generated from the latest property data
            and historical scrape activity.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # MARKET SNAPSHOT
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Listings",
            f"{market_summary['total_listings']:,}",
        )

    with col2:
        st.metric(
            "Average Price",
            f"${market_summary['average_price']:,.0f}",
        )

    with col3:
        st.metric(
            "Median Price",
            f"${market_summary['median_price']:,.0f}",
        )

    with col4:
        st.metric(
            "Active Listings",
            f"{market_summary['active_listings']:,}",
            f"{market_summary['active_percentage']:.1f}% of market",
        )

    # --------------------------------------------------------
    # MARKET SIGNALS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Pricing Signal**")

        st.write(
            f"{pricing_insight['percentage']:.1f}% of listings "
            f"are priced in the "
            f"**{pricing_insight['dominant_segment']}** range."
        )

    with col2:
        st.markdown("**Location Signal**")

        st.write(
            f"**{location_insight['highest_average_price_area']}** "
            f"has the highest average listing price at "
            f"${location_insight['highest_average_price']:,.0f}."
        )

    with col3:
        st.markdown("**Inventory Signal**")

        st.write(
            f"**{inventory_insight['dominant_status']}** "
            f"accounts for "
            f"{inventory_insight['dominant_percentage']:.1f}% "
            f"of current listings."
        )

    # --------------------------------------------------------
    # MARKET MOVEMENT
    # --------------------------------------------------------

    st.markdown("**Market Movement**")

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
                movement_insight[
                    "availability_changes"
                ],
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
        # MARKET PRICING
        # ========================================================

        price_stats = analyze_price_statistics(properties)

        st.markdown(
            '<div class="section-title">Market Pricing</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Core pricing indicators across the current market.
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average Price",
                f"${price_stats['average']:,.0f}",
            )

        with col2:
            st.metric(
                "Median Price",
                f"${price_stats['median']:,.0f}",
            )

        with col3:
            st.metric(
                "Highest Price",
                f"${price_stats['highest']:,.0f}",
            )

        with col4:
            st.metric(
                "Lowest Price",
                f"${price_stats['lowest']:,.0f}",
            )

            # ========================================================
        # PRICE PER SQFT
        # ========================================================

        price_per_sqft = analyze_price_per_sqft_statistics(
            properties
        )

        st.markdown(
            '<div class="section-title">Price per Sqft</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Measures how property prices compare relative to
                available living space.
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average",
                f"${price_per_sqft['average']:,.0f}/sqft",
            )

        with col2:
            st.metric(
                "Median",
                f"${price_per_sqft['median']:,.0f}/sqft",
            )

        with col3:
            st.metric(
                "Weighted Average",
                f"${price_per_sqft['weighted']:,.0f}/sqft",
            )
            # ========================================================
        # PROPERTY TYPE ANALYSIS
        # ========================================================

        price_by_type = analyze_price_by_property_type(
            properties
        )

        type_df = pd.DataFrame.from_dict(
            price_by_type,
            orient="index",
        )

        type_df = (
            type_df
            .reset_index()
            .rename(
                columns={
                    "index": "Property Type",
                    "average_price": "Average Price",
                }
            )
            .sort_values(
                "Average Price",
                ascending=False,
            )
        )

        st.markdown(
            '<div class="section-title">Property Type Analysis</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Compare pricing across different property types.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.bar_chart(
            type_df.set_index("Property Type")["Average Price"],
            use_container_width=True,
        )       
            # ========================================================
        # MARKET VALUE BY NEIGHBORHOOD
        # ========================================================

        market_value = analyze_market_value_by_area(
            properties
        )

        market_value_df = pd.DataFrame.from_dict(
            market_value,
            orient="index",
        )

        market_value_df = (
            market_value_df
            .reset_index()
            .rename(
                columns={
                    "index": "Neighborhood",
                    "total_market_value": "Total Market Value",
                }
            )
            .sort_values(
                "Total Market Value",
                ascending=False,
            )
        )

        st.markdown(
            '<div class="section-title">Market Value by Neighborhood</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Total listed property value currently represented
                in each neighborhood.
            </div>
            """,
            unsafe_allow_html=True,
        )

        market_value_fig = go.Figure(
        data=[
            go.Bar(
                x=market_value_df["Total Market Value"],
                y=market_value_df["Neighborhood"],
                orientation="h",
                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>Total Market Value: $%{x:,.0f}"
                    "<extra></extra>"
                ),
            )
        ]
    )

        market_value_fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            xaxis=dict(
                title="Total Market Value",
                tickprefix="$",
                tickformat=",.0f",
            ),
            yaxis=dict(
                title="",
            ),
            showlegend=False,
        )

        st.plotly_chart(
                market_value_fig,
                use_container_width=True,
                config={
                    "staticPlot": True,
                    "displayModeBar": False,
                },
            )
            # ========================================================
        # AREA INTELLIGENCE
        # ========================================================

        area_intelligence = analyze_area_intelligence(
            properties
        )

        area_df = pd.DataFrame.from_dict(
            area_intelligence,
            orient="index",
        )

        area_df = (
            area_df
            .reset_index()
            .rename(
                columns={
                    "index": "Neighborhood",
                    "listings": "Listings",
                    "average_price": "Average Price",
                    "median_price": "Median Price",
                    "weighted_price_per_sqft": "Price / Sqft",
                    "average_sqft": "Average Size",
                    "total_market_value": "Market Value",
                }
            )
            .sort_values(
                "Average Price",
                ascending=False,
            )
        )

        st.markdown(
            '<div class="section-title">Area Intelligence</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Compare key market indicators across neighborhoods.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.dataframe(
            area_df,
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
                "Price / Sqft": st.column_config.NumberColumn(
                    "Price / Sqft",
                    format="$%,.0f",
                ),
                "Average Size": st.column_config.NumberColumn(
                    "Average Size",
                    format="%,.0f sqft",
                ),
                "Market Value": st.column_config.NumberColumn(
                    "Market Value",
                    format="$%,.0f",
                ),
            },
        )
            # ========================================================
        # PRICE SEGMENTS
        # ========================================================

        price_segments = analyze_price_segments(properties)

        segment_df = pd.DataFrame(
            list(price_segments.items()),
            columns=["Price Range", "Listings"],
        )

        total_listings = segment_df["Listings"].sum()

        segment_df["Percentage"] = (
            segment_df["Listings"]
            / total_listings
            * 100
        )

        st.markdown(
            '<div class="section-title">Price Distribution</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Distribution of current listings across price ranges.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.bar_chart(
            segment_df.set_index("Price Range")["Listings"],
            use_container_width=True,
        )

        st.dataframe(
            segment_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Price Range": st.column_config.TextColumn(
                    "Price Range",
                ),
                "Listings": st.column_config.NumberColumn(
                    "Listings",
                    format="%d",
                ),
                "Percentage": st.column_config.NumberColumn(
                    "Market Share",
                    format="%.1f%%",
                ),
            },
        )
            # ========================================================
        # INVENTORY STATUS
        # ========================================================

        availability = analyze_availability(properties)
        availability = analyze_availability(
            properties
        )

        availability_df = pd.DataFrame(
            list(availability.items()),
            columns=[
                "Status",
                "Listings",
            ],
        )

        st.markdown(
            '<div class="section-title">Inventory Status</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                Current distribution of listings by market status.
            </div>
            """,
            unsafe_allow_html=True,
        )

        availability_fig = go.Figure(
            data=[
                go.Pie(
                    labels=availability_df["Status"],
                    values=availability_df["Listings"],
                    hole=0.58,
                    textinfo="label+percent",
                )
            ]
        )

        availability_fig.update_layout(
            height=380,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            showlegend=True,
        )

        st.plotly_chart(
            availability_fig,
            use_container_width=True,
            config={
                "staticPlot": True,
                "displayModeBar": False,
            },
        )