import streamlit as st

from dashboard.data import get_properties
from dashboard.views.overview import render_overview
from dashboard.views.trends import render_trends
from dashboard.views.changes import render_changes
from dashboard.views.history import render_history
from dashboard.views.analysis import render_analysis
from dashboard.views.reports import render_reports
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Homestead Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================
theme_base = st.get_option("theme.base")

if theme_base == "dark":
    sidebar_background = "#171b22"
    sidebar_border = "rgba(255, 255, 255, 0.10)"
else:
    sidebar_background = "#f3f4f6"
    sidebar_border = "rgba(0, 0, 0, 0.10)"



st.markdown(
    """
    <style>

   .stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
section[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
    border-right: 1px solid rgba(128, 128, 128, 0.25);
}
section[data-testid="stSidebar"] * {
    color: var(--text-color);
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.brand-title {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-color);
    margin-bottom: 0.15rem;
}

.brand-subtitle {
    color: var(--secondary-text-color);
    font-size: 0.95rem;
}

.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    border: 1px solid var(--primary-color);
    color: var(--primary-color);
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
}

.live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #10b981;
    display: inline-block;
}

.section-title {
    color: var(--text-color);
    font-size: 1.25rem;
    font-weight: 750;
    margin-top: 2rem;
    margin-bottom: 0.2rem;
}

.section-description {
    color: var(--secondary-text-color);
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

df = get_properties()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        ">
            🏠 Homestead
        </div>

        <div style="
            font-size: 0.8rem;
            color: #9ca3af;
            margin-bottom: 1.5rem;
        ">
            Market Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Go to",
        [
            "Overview",
            "Market Trends",
            "Market Activity",
            "Market History",
            "Market Analysis",
            "Reports",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption(
        f"Database records: {len(df):,}"
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "Overview":

    render_overview(df)


elif page == "Market Trends":

    render_trends()


elif page == "Market Activity":

    render_changes()

elif page == "Market History":

    render_history(df)

elif page == "Market Analysis":

    render_analysis()

elif page == "Reports":

    render_reports()