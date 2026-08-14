import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_overview(df):

    # ========================================================
    # THEME
    # ========================================================

    theme_base = st.get_option("theme.base")

    if theme_base == "dark":
        text_color = "#f9fafb"
        grid_color = "rgba(255, 255, 255, 0.12)"
    else:
        text_color = "#111827"
        grid_color = "rgba(0, 0, 0, 0.10)"

    transparent = "rgba(0, 0, 0, 0)"

    static_chart_config = {
        "staticPlot": True,
        "displayModeBar": False,
    }

    # ========================================================
    # FILTERS
    # ========================================================

    with st.sidebar:

        st.markdown("### Market Filters")

        neighborhoods = sorted(
            df["neighborhood"].dropna().unique().tolist()
        )

        property_types = sorted(
            df["property_type"].dropna().unique().tolist()
        )

        availability_options = sorted(
            df["availability"].dropna().unique().tolist()
        )

        bedroom_options = sorted(
            df["bedrooms"].dropna().unique().tolist()
        )

        selected_neighborhood = st.multiselect(
            "Neighborhood",
            neighborhoods,
            placeholder="All neighborhoods",
        )

        selected_property_types = st.multiselect(
            "Property Type",
            property_types,
            placeholder="All property types",
        )

        selected_availability = st.multiselect(
            "Availability",
            availability_options,
            placeholder="All statuses",
        )

        selected_bedrooms = st.multiselect(
            "Bedrooms",
            bedroom_options,
            placeholder="All bedroom counts",
        )

        min_price = float(df["price"].min())
        max_price = float(df["price"].max())

        price_range = st.slider(
            "Price Range",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=25000.0,
            format="$%d",
        )

        st.divider()

        

    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered_df = df.copy()

    if selected_neighborhood:
        filtered_df = filtered_df[
            filtered_df["neighborhood"].isin(
                selected_neighborhood
            )
        ]

    if selected_property_types:
        filtered_df = filtered_df[
            filtered_df["property_type"].isin(
                selected_property_types
            )
        ]

    if selected_availability:
        filtered_df = filtered_df[
            filtered_df["availability"].isin(
                selected_availability
            )
        ]

    if selected_bedrooms:
        filtered_df = filtered_df[
            filtered_df["bedrooms"].isin(
                selected_bedrooms
            )
        ]

    filtered_df = filtered_df[
        (filtered_df["price"] >= price_range[0])
        & (filtered_df["price"] <= price_range[1])
    ]

    # ========================================================
    # EMPTY FILTER RESULT
    # ========================================================

    if filtered_df.empty:

        st.title("Homestead Intelligence")

        st.caption(
            "Real Estate Market Intelligence Dashboard"
        )

        st.markdown(
            '<span class="live-badge">'
            '<span class="live-dot"></span>'
            'LIVE DATA'
            '</span>',
            unsafe_allow_html=True,
        )

        st.warning(
            "No properties match the selected filters."
        )

        return

    # ========================================================
    # HEADER
    # ========================================================

    st.title("Homestead Intelligence")

    st.caption(
        "Real Estate Market Intelligence Dashboard"
    )

    st.markdown(
        '<span class="live-badge">'
        '<span class="live-dot"></span>'
        'LIVE DATA'
        '</span>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_properties = len(filtered_df)

    average_price = filtered_df["price"].mean()
    median_price = filtered_df["price"].median()

    active_count = len(
        filtered_df[
            filtered_df["availability"] == "ACTIVE"
        ]
    )

    # ========================================================
    # KPI CARDS
    # ========================================================

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "Properties",
            f"{total_properties:,}",
        )

    with kpi2:
        st.metric(
            "Average Price",
            f"${average_price:,.0f}",
        )

    with kpi3:
        st.metric(
            "Median Price",
            f"${median_price:,.0f}",
        )

    with kpi4:
        st.metric(
            "Active Listings",
            f"{active_count:,}",
        )

    # ========================================================
    # MARKET ANALYTICS
    # ========================================================

    st.markdown(
        '<div class="section-title">Market Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Explore pricing patterns across the current market.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # ROW 1
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # AVERAGE PRICE BY PROPERTY TYPE
    # --------------------------------------------------------

    with col1:

        avg_price_type = (
            filtered_df
            .groupby("property_type")["price"]
            .mean()
            .sort_values(ascending=False)
        )

        st.subheader("Average Price by Property Type")

        property_type_fig = go.Figure(
            data=[
                go.Bar(
                    x=avg_price_type.index,
                    y=avg_price_type.values,
                    hovertemplate=(
                        "<b>%{x}</b>"
                        "<br>Average Price: $%{y:,.0f}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        property_type_fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=40,
            ),
            font=dict(
                color=text_color,
            ),
            xaxis=dict(
                title="",
            ),
            yaxis=dict(
                title="Average Price",
                tickprefix="$",
                tickformat=",.0f",
                gridcolor=grid_color,
            ),
            plot_bgcolor=transparent,
            paper_bgcolor=transparent,
            showlegend=False,
        )

        st.plotly_chart(
            property_type_fig,
            use_container_width=True,
            config=static_chart_config,
        )

    # --------------------------------------------------------
    # AVERAGE PRICE BY NEIGHBORHOOD
    # --------------------------------------------------------

    with col2:

        avg_price_neighborhood = (
            filtered_df
            .groupby("neighborhood")["price"]
            .mean()
            .sort_values(ascending=True)
        )

        st.subheader("Average Price by Neighborhood")

        neighborhood_fig = go.Figure(
            data=[
                go.Bar(
                    x=avg_price_neighborhood.values,
                    y=avg_price_neighborhood.index,
                    orientation="h",
                    hovertemplate=(
                        "<b>%{y}</b>"
                        "<br>Average Price: $%{x:,.0f}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        neighborhood_fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            font=dict(
                color=text_color,
            ),
            xaxis=dict(
                title="Average Price",
                tickprefix="$",
                tickformat=",.0f",
                gridcolor=grid_color,
            ),
            yaxis=dict(
                title="",
            ),
            plot_bgcolor=transparent,
            paper_bgcolor=transparent,
            showlegend=False,
        )

        st.plotly_chart(
            neighborhood_fig,
            use_container_width=True,
            config=static_chart_config,
        )

    # ========================================================
    # ROW 2
    # ========================================================

    col3, col4 = st.columns(2)

    # --------------------------------------------------------
    # PRICE SEGMENTS
    # --------------------------------------------------------

    with col3:

        price_segments = pd.cut(
            filtered_df["price"],
            bins=[
                0,
                500_000,
                1_000_000,
                1_500_000,
                2_500_000,
                float("inf"),
            ],
            labels=[
                "Under $500K",
                "$500K - $999K",
                "$1M - $1.49M",
                "$1.5M - $2.49M",
                "$2.5M+",
            ],
            include_lowest=True,
        )

        segment_counts = (
            price_segments
            .value_counts()
            .sort_index()
        )

        st.subheader("Price Segments")

        segment_fig = go.Figure(
            data=[
                go.Bar(
                    x=segment_counts.index.astype(str),
                    y=segment_counts.values,
                    hovertemplate=(
                        "<b>%{x}</b>"
                        "<br>Listings: %{y:,}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        segment_fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=60,
            ),
            font=dict(
                color=text_color,
            ),
            xaxis=dict(
                title="Price Range",
            ),
            yaxis=dict(
                title="Listings",
                tickformat=",",
                gridcolor=grid_color,
            ),
            plot_bgcolor=transparent,
            paper_bgcolor=transparent,
            showlegend=False,
        )

        st.plotly_chart(
            segment_fig,
            use_container_width=True,
            config=static_chart_config,
        )

    # --------------------------------------------------------
    # LISTING AVAILABILITY
    # --------------------------------------------------------

    with col4:

        availability_counts = (
            filtered_df["availability"]
            .value_counts()
        )

        st.subheader("Listing Availability")

        availability_fig = go.Figure(
            data=[
                go.Pie(
                    labels=availability_counts.index,
                    values=availability_counts.values,
                    hole=0.58,
                    textinfo="label+percent",
                    textfont=dict(
                        color=text_color
                    ),
                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>Listings: %{value:,}"
                        "<br>Share: %{percent}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        availability_fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            font=dict(
                color=text_color,
            ),
            legend=dict(
                font=dict(
                    color=text_color
                )
            ),
            paper_bgcolor=transparent,
            plot_bgcolor=transparent,
            showlegend=True,
        )

        st.plotly_chart(
            availability_fig,
            use_container_width=True,
            config=static_chart_config,
        )

    # ========================================================
    # ROW 3
    # ========================================================

    col5, col6 = st.columns(2)

    # --------------------------------------------------------
    # AVERAGE PRICE PER SQFT
    # --------------------------------------------------------

    with col5:

        sqft_df = filtered_df[
            filtered_df["sqft"] > 0
        ].copy()

        if not sqft_df.empty:

            price_sqft = (
                sqft_df
                .assign(
                    price_per_sqft=lambda x:
                        x["price"] / x["sqft"]
                )
                .groupby("neighborhood")[
                    "price_per_sqft"
                ]
                .mean()
                .sort_values(ascending=True)
            )

            st.subheader("Average Price per Sqft")

            price_sqft_fig = go.Figure(
                data=[
                    go.Bar(
                        x=price_sqft.values,
                        y=price_sqft.index,
                        orientation="h",
                        hovertemplate=(
                            "<b>%{y}</b>"
                            "<br>Average Price/Sqft: "
                            "$%{x:,.0f}"
                            "<extra></extra>"
                        ),
                    )
                ]
            )

            price_sqft_fig.update_layout(
                height=420,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20,
                ),
                font=dict(
                    color=text_color,
                ),
                xaxis=dict(
                    title="Average Price / Sqft",
                    tickprefix="$",
                    tickformat=",.0f",
                    gridcolor=grid_color,
                ),
                yaxis=dict(
                    title="",
                ),
                plot_bgcolor=transparent,
                paper_bgcolor=transparent,
                showlegend=False,
            )

            st.plotly_chart(
                price_sqft_fig,
                use_container_width=True,
                config=static_chart_config,
            )

        else:

            st.subheader("Average Price per Sqft")
            st.info(
                "No valid square-footage data is available "
                "for the selected properties."
            )

    # --------------------------------------------------------
    # AVERAGE PRICE BY BEDROOMS
    # --------------------------------------------------------

    with col6:

        bedroom_prices = (
            filtered_df
            .groupby("bedrooms")["price"]
            .mean()
            .sort_index()
        )

        st.subheader("Average Price by Bedrooms")

        bedroom_fig = go.Figure(
            data=[
                go.Bar(
                    x=bedroom_prices.index.astype(str),
                    y=bedroom_prices.values,
                    hovertemplate=(
                        "<b>%{x} bedrooms</b>"
                        "<br>Average Price: $%{y:,.0f}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        bedroom_fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=40,
            ),
            font=dict(
                color=text_color,
            ),
            xaxis=dict(
                title="Bedrooms",
            ),
            yaxis=dict(
                title="Average Price",
                tickprefix="$",
                tickformat=",.0f",
                gridcolor=grid_color,
            ),
            plot_bgcolor=transparent,
            paper_bgcolor=transparent,
            showlegend=False,
        )

        st.plotly_chart(
            bedroom_fig,
            use_container_width=True,
            config=static_chart_config,
        )

    # ========================================================
    # PROPERTY LISTINGS
    # ========================================================

    st.markdown(
        '<div class="section-title">Property Listings</div>',
        unsafe_allow_html=True,
    )

    display_df = filtered_df[
        [
            "title",
            "price",
            "neighborhood",
            "bedrooms",
            "bathrooms",
            "sqft",
            "property_type",
            "availability",
        ]
    ].copy()

    display_df["price"] = display_df["price"].map(
        lambda x: f"${x:,.0f}"
    )

    display_df["sqft"] = display_df["sqft"].map(
        lambda x: (
            f"{x:,.0f} sqft"
            if pd.notna(x)
            else "N/A"
        )
    )

    display_df = display_df.rename(
        columns={
            "title": "Property",
            "price": "Price",
            "neighborhood": "Neighborhood",
            "bedrooms": "Beds",
            "bathrooms": "Baths",
            "sqft": "Sqft",
            "property_type": "Property Type",
            "availability": "Status",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=520,
    )