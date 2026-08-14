import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from analysis.market_trends import (
    get_market_snapshots,
    get_availability_trends,
    get_market_trend_summary,
)


def render_trends():

    # ========================================================
    # THEME COLORS
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
    # HEADER
    # ========================================================

    st.title("Market Trends")

    st.markdown(
        """
        <div class="section-description">
            Track how the real estate market changes across
            successive scrape runs.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD TREND DATA
    # ========================================================

    snapshots = get_market_snapshots()
    summary = get_market_trend_summary()

    if not snapshots or not summary:
        st.warning(
            "Not enough scrape history to display market trends."
        )
        return

    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    price_change = summary["price_change"]
    price_change_percent = summary[
        "price_change_percent"
    ]

    if price_change > 0:
        price_delta = f"+${price_change:,.0f}"
    elif price_change < 0:
        price_delta = f"-${abs(price_change):,.0f}"
    else:
        price_delta = "$0"

    if price_change_percent > 0:
        percent_delta = (
            f"+{price_change_percent:.2f}%"
        )
    elif price_change_percent < 0:
        percent_delta = (
            f"{price_change_percent:.2f}%"
        )
    else:
        percent_delta = "0.00%"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Latest Average Price",
            f"${summary['latest_average_price']:,.0f}",
        )

    with col2:
        st.metric(
            "Price Change",
            price_delta,
            percent_delta,
        )

    with col3:
        st.metric(
            "Latest Property Count",
            f"{summary['latest_property_count']:,}",
        )

    with col4:
        st.metric(
            "Scrape Runs",
            f"{len(snapshots):,}",
        )

    # ========================================================
    # BUILD TREND DATAFRAME
    # ========================================================

    trend_df = pd.DataFrame(
        snapshots,
        columns=[
            "scrape_run_id",
            "scraped_at",
            "property_count",
            "average_price",
        ],
    )

    trend_df["scraped_at"] = pd.to_datetime(
        trend_df["scraped_at"]
    )

    trend_df = trend_df.sort_values(
        "scraped_at"
    )

    # ========================================================
    # PRICE TREND
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Average Market Price'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Movement in average asking price across scrape runs.
        </div>
        """,
        unsafe_allow_html=True,
    )

    price_fig = go.Figure()

    price_fig.add_trace(
        go.Scatter(
            x=trend_df["scraped_at"],
            y=trend_df["average_price"],
            mode="lines+markers",
            name="Average Price",
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate=(
                "<b>%{x|%d %b %Y, %I:%M %p}</b>"
                "<br>Average Price: $%{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    price_fig.update_layout(
        height=380,
        dragmode=False,
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
            title="",
            showgrid=False,
            tickformat="%d %b",
        ),
        yaxis=dict(
            title="Average Price",
            tickprefix="$",
            tickformat=",.0f",
            gridcolor=grid_color,
        ),
        plot_bgcolor=transparent,
        paper_bgcolor=transparent,
        hovermode="x unified",
        showlegend=False,
    )

    st.plotly_chart(
        price_fig,
        use_container_width=True,
        config=static_chart_config,
    )

    # ========================================================
    # PROPERTY COUNT TREND
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Market Inventory'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
            Number of tracked properties across scrape runs.
        </div>
        """,
        unsafe_allow_html=True,
    )

    property_count_fig = go.Figure()

    property_count_fig.add_trace(
        go.Scatter(
            x=trend_df["scraped_at"],
            y=trend_df["property_count"],
            mode="lines+markers",
            name="Properties",
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate=(
                "<b>%{x|%d %b %Y, %I:%M %p}</b>"
                "<br>Properties: %{y:,}"
                "<extra></extra>"
            ),
        )
    )

    property_count_fig.update_layout(
        height=380,
        dragmode=False,
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
            title="",
            showgrid=False,
            tickformat="%d %b",
        ),
        yaxis=dict(
            title="Properties",
            tickformat=",",
            gridcolor=grid_color,
        ),
        plot_bgcolor=transparent,
        paper_bgcolor=transparent,
        hovermode="x unified",
        showlegend=False,
    )

    st.plotly_chart(
        property_count_fig,
        use_container_width=True,
        config=static_chart_config,
    )

    # ========================================================
    # AVAILABILITY TREND
    # ========================================================

    availability_rows = get_availability_trends()

    if availability_rows:

        availability_df = pd.DataFrame(
            availability_rows,
            columns=[
                "scrape_run_id",
                "availability",
                "property_count",
            ],
        )

        availability_df = availability_df.merge(
            trend_df[
                [
                    "scrape_run_id",
                    "scraped_at",
                ]
            ],
            on="scrape_run_id",
            how="left",
        )

        availability_df = availability_df.sort_values(
            "scraped_at"
        )

        st.markdown(
            '<div class="section-title">'
            'Inventory by Status'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="section-description">
                How tracked properties are distributed across
                market statuses over time.
            </div>
            """,
            unsafe_allow_html=True,
        )

        availability_fig = go.Figure()

        statuses = sorted(
            availability_df["availability"]
            .dropna()
            .unique()
        )

        for status in statuses:

            status_df = availability_df[
                availability_df["availability"] == status
            ]

            availability_fig.add_trace(
                go.Scatter(
                    x=status_df["scraped_at"],
                    y=status_df["property_count"],
                    mode="lines+markers",
                    name=status,
                    line=dict(width=2.5),
                    marker=dict(size=7),
                    hovertemplate=(
                        "<b>%{x|%d %b %Y, %I:%M %p}</b>"
                        f"<br>{status}: "
                        "%{y:,} properties"
                        "<extra></extra>"
                    ),
                )
            )

        availability_fig.update_layout(
            height=420,
            dragmode=False,
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
                title="",
                showgrid=False,
                tickformat="%d %b",
            ),
            yaxis=dict(
                title="Properties",
                tickformat=",",
                gridcolor=grid_color,
            ),
            plot_bgcolor=transparent,
            paper_bgcolor=transparent,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
            ),
        )

        st.plotly_chart(
            availability_fig,
            use_container_width=True,
            config=static_chart_config,
        )

    # ========================================================
    # TREND PERIOD
    # ========================================================

    st.markdown(
        '<div class="section-title">Trend Period</div>',
        unsafe_allow_html=True,
    )

    st.write(
        f"First scrape: **{summary['first_date']}**"
    )

    st.write(
        f"Latest scrape: **{summary['latest_date']}**"
    )