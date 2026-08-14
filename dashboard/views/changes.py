import streamlit as st

from analysis.change_detector import (
    detect_changes,
    get_change_history,
)


def render_changes():

    # ========================================================
    # HEADER
    # ========================================================

    st.title("🔄 Market Activity")

    st.markdown(
        """
        <div class="section-description">
            Track new listings, price changes, availability changes,
            and removed properties between scrape runs.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD CHANGES
    # ========================================================

    changes = detect_changes()
    history = get_change_history()

    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    new_count = len(changes["new_listings"])
    price_count = len(changes["price_changes"])
    availability_count = len(
        changes["availability_changes"]
    )
    removed_count = len(
        changes["removed_listings"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "New Listings",
            f"{new_count:,}",
        )

    with col2:
        st.metric(
            "Price Changes",
            f"{price_count:,}",
        )

    with col3:
        st.metric(
            "Availability Changes",
            f"{availability_count:,}",
        )

    with col4:
        st.metric(
            "Removed Listings",
            f"{removed_count:,}",
        )

    # ========================================================
    # SCRAPE PERIOD
    # ========================================================

    if changes.get("latest_scrape"):

        st.markdown(
            '<div class="section-title">Market Activity Period</div>',
            unsafe_allow_html=True,
        )

        latest_scrape = changes["latest_scrape"]
        previous_scrape = changes.get("previous_scrape")

        if previous_scrape:
            st.write(
                f"Previous Market Snapshot: **{previous_scrape}**"
            )

        st.write(
            f"Current Market Snapshot: **{latest_scrape}**"
        )

    # ========================================================
    # NEW LISTINGS
    # ========================================================

    st.markdown(
        '<div class="section-title">New Listings</div>',
        unsafe_allow_html=True,
    )

    if changes["new_listings"]:

        new_df = changes["new_listings"]

        st.dataframe(
            new_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No new listings detected between the latest scrape runs."
        )

    # ========================================================
    # PRICE CHANGES
    # ========================================================

    st.markdown(
        '<div class="section-title">Price Changes</div>',
        unsafe_allow_html=True,
    )

    if changes["price_changes"]:

        price_df = changes["price_changes"]

        st.dataframe(
            price_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No price changes detected between the latest scrape runs."
        )

    # ========================================================
    # AVAILABILITY CHANGES
    # ========================================================

    st.markdown(
        '<div class="section-title">Availability Changes</div>',
        unsafe_allow_html=True,
    )

    if changes["availability_changes"]:

        availability_df = changes[
            "availability_changes"
        ]

        st.dataframe(
            availability_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No availability changes detected between the latest scrape runs."
        )

    # ========================================================
    # REMOVED LISTINGS
    # ========================================================

    st.markdown(
        '<div class="section-title">Removed Listings</div>',
        unsafe_allow_html=True,
    )

    if changes["removed_listings"]:

        removed_df = changes["removed_listings"]

        st.dataframe(
            removed_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No removed listings detected between the latest scrape runs."
        )

    # ========================================================
    # CHANGE HISTORY
    # ========================================================

    st.markdown(
        '<div class="section-title">Change History</div>',
        unsafe_allow_html=True,
    )

    if history:

        history_df = history.copy()

        # Rename database-oriented fields
        # into dashboard-friendly names.
        history_df = [
            {
                "Date": change["detected_at"],
                "Change Type": change["change_type"],
                "Property": change["title"],
                "Previous Value": change["old_value"],
                "New Value": change["new_value"],
                "Change": change["change_amount"],
                "URL": change["url"],
            }
            for change in history_df
        ]

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No change history recorded yet."
        )