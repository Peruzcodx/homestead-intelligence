import streamlit as st
import pandas as pd

from analysis.history_analysis import (
    get_property_history,
    get_property_changes,
)


def render_history(df):

    # ========================================================
    # HEADER
    # ========================================================

    st.title("Market History")

    st.markdown(
        """
        <div class="section-description">
           Track pricing and availability trends for an
           individual property across market observations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # PROPERTY SELECTION
    # ========================================================

    if df.empty:
        st.warning("No properties are available.")
        return

    property_options = (
        df[["title", "url"]]
        .dropna(subset=["title", "url"])
        .drop_duplicates()
    )

    selected_property = st.selectbox(
        "Select Property",
        property_options["title"].tolist(),
    )

    selected_url = property_options.loc[
        property_options["title"] == selected_property,
        "url",
    ].iloc[0]

    # ========================================================
    # CURRENT PROPERTY DETAILS
    # ========================================================

    property_row = df[
        df["url"] == selected_url
    ].iloc[0]

    st.markdown(
        '<div class="section-title">Property Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Market Price",
            f"${property_row['price']:,.0f}"
            if pd.notna(property_row["price"])
            else "N/A",
        )

    with col2:
        st.metric(
            "Availability",
            property_row["availability"]
            if pd.notna(property_row["availability"])
            else "N/A",
        )

    with col3:
        st.metric(
            "Bedrooms",
            f"{property_row['bedrooms']:g}"
            if pd.notna(property_row["bedrooms"])
            else "N/A",
        )

    with col4:
        st.metric(
            "Property Type",
            property_row["property_type"]
            if pd.notna(property_row["property_type"])
            else "N/A",
        )

    location_parts = [
        property_row["street"],
        property_row["city"],
        property_row["state"],
        property_row["zip"],
    ]

    location = ", ".join(
        str(value)
        for value in location_parts
        if pd.notna(value) and str(value).strip()
    )

    st.caption(location)

    # ========================================================
    # LOAD HISTORY
    # ========================================================

    history = get_property_history(selected_url)

    if not history:
        st.info(
            "No historical observations are available for this property."
        )
        return

    history_df = pd.DataFrame(
        history,
        columns=[
            "price",
            "availability",
            "scraped_at",
        ],
    )

    history_df["scraped_at"] = pd.to_datetime(
        history_df["scraped_at"]
    )

    history_df = history_df.sort_values(
        "scraped_at"
    )

    # ========================================================
    # HISTORY SUMMARY
    # ========================================================

    changes = get_property_changes(selected_url)

    if changes:

        st.markdown(
            '<div class="section-title">Pricing Summary</div>',
            unsafe_allow_html=True,
        )

        change_col1, change_col2, change_col3, change_col4 = (
            st.columns(4)
        )

        with change_col1:
            first_price = changes["first_price"]

            st.metric(
                "Initial Market Price",
                f"${first_price:,.0f}"
                if first_price is not None
                else "N/A",
            )

        with change_col2:
            latest_price = changes["latest_price"]

            st.metric(
                "Current Market Price",
                f"${latest_price:,.0f}"
                if latest_price is not None
                else "N/A",
            )

        with change_col3:
            price_change = changes["price_change"]

            if price_change is not None:
                st.metric(
                    "Price Movement",
                    f"${price_change:,.0f}",
                )
            else:
                st.metric(
                    "Price Movement",
                    "N/A",
                )

        with change_col4:
            percent_change = changes[
                "price_change_percent"
            ]

            if percent_change is not None:
                st.metric(
                    "Price Change %",
                    f"{percent_change:.2f}%",
                )
            else:
                st.metric(
                    "Price Change %",
                    "N/A",
                    )
        # ========================================================
    # PRICE HISTORY
    # ========================================================

    st.markdown(
        '<div class="section-title">Pricing Trend</div>',
        unsafe_allow_html=True,
    )

    price_history = history_df[
        ["scraped_at", "price"]
    ].dropna(subset=["price"])

    if len(price_history) >= 2:

        import plotly.graph_objects as go

        min_price = price_history["price"].min()
        max_price = price_history["price"].max()

        price_range = max_price - min_price

        # Prevent a zero-height axis when all prices are identical
        if price_range == 0:
            padding = max_price * 0.001
        else:
            padding = price_range * 0.20

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=price_history["scraped_at"],
                y=price_history["price"],
                mode="lines+markers",
                hovertemplate=(
                    "<b>%{x|%d %b %Y, %I:%M %p}</b>"
                    "<br>Price: $%{y:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            height=400,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            xaxis_title=None,
            yaxis_title="Market Price ($)",
            yaxis=dict(
                range=[
                    min_price - padding,
                    max_price + padding,
                ],
                tickformat="$,.0f",
            ),
            hovermode="x unified",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "staticPlot": True,
            },
        )

    elif len(price_history) == 1:

        st.info(
            "Only one price observation is available. "
            "A price trend will appear after another market observation."
        )

    else:

        st.info(
            "No price observations are available."
        )

    # ========================================================
    # AVAILABILITY HISTORY
    # ========================================================

    st.markdown(
        '<div class="section-title">Availability Timeline</div>',
        unsafe_allow_html=True,
    )

    availability_history = history_df[
        ["scraped_at", "availability"]
    ].copy()

    availability_history = (
        availability_history
        .dropna(subset=["availability"])
        .drop_duplicates()
    )

    if availability_history.empty:

        st.info(
            "No availability history is available."
        )

    else:

        st.dataframe(
            availability_history.rename(
                columns={
                    "scraped_at": "Date",
                    "availability": "Availability",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================
    # HISTORICAL OBSERVATIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">Market Observations</div>',
        unsafe_allow_html=True,
    )

    display_history = history_df.copy()

    display_history["scraped_at"] = (
        display_history["scraped_at"]
        .dt.strftime("%d %b %Y, %I:%M %p")
    )

    display_history["price"] = (
        display_history["price"]
        .apply(
            lambda value:
            f"${value:,.0f}"
            if pd.notna(value)
            else "N/A"
        )
    )

    display_history = display_history.rename(
        columns={
            "scraped_at": "Date",
            "price": "Price",
            "availability": "Availability",
        }
    )

    st.dataframe(
        display_history,
        use_container_width=True,
        hide_index=True,
    )

    # ========================================================
    # OBSERVATION PERIOD
    # ========================================================

    st.markdown(
        '<div class="section-title">Market Observation Period</div>',
        unsafe_allow_html=True,
    )

    st.write(
        f"First recorded: **{changes['first_seen']}**"
        if changes
        else "First observed: **N/A**"
    )

    st.write(
        f"Latest recorded: **{changes['last_seen']}**"
        if changes
        else "Latest recorded: **N/A**"
    )

    st.write(
        f"Market observations: "
        f"**{len(history):,}**"
    )