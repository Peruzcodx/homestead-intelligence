import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
    background-color: #171b22 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.10);
    z-index: 999999 !important;
}

section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div > div {
    background-color: #171b22 !important;
}

section[data-testid="stSidebar"] * {
    color: var(--text-color);
}

/* ============================================================
   SIDEBAR NAVIGATION
   ============================================================ */

.sidebar-section-title {
    color: #9ca3af;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.5rem 0 0.75rem 0;
}
/* ============================================================
   SIDEBAR NAVIGATION
   ============================================================ */

.sidebar-section-title {
    color: #9ca3af;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.5rem 0 0.75rem 0;
}
/* Navigation button */
section[data-testid="stSidebar"] div.stButton {
    margin-bottom: 0.15rem;
}
section[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    min-height: 34px !important;
    border-radius: 8px !important;
    border: 1px solid transparent !important;
    background-color: transparent !important;
    color: #d1d5db !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    text-align: left !important;
    padding: 0.3rem 0.6rem !important;
    box-shadow: none !important;
}

/* Control navigation button internal content spacing */
section[data-testid="stSidebar"] div.stButton > button > div {
    gap: 0.35rem !important;
    justify-content: flex-start !important;
}

    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        color 0.15s ease !important;
}

/* Hover */
section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #222832 !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
    color: #ffffff !important;
}

/* Active button */
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background-color: #26313d !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
}

/* Focus */
section[data-testid="stSidebar"] div.stButton > button:focus {
    outline: none !important;
    box-shadow: none !important;
}
@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        background-color: #171b22 !important;
        z-index: 999999 !important;
        box-shadow: 8px 0 25px rgba(0, 0, 0, 0.30);

        max-height: 100vh !important;
        overflow: hidden !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #171b22 !important;

        max-height: 100vh !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;

        box-sizing: border-box !important;
    }

    section[data-testid="stSidebar"] > div > div {
        background-color: #171b22 !important;

        height: auto !important;
        min-height: auto !important;
    }

    section[data-testid="stSidebar"] > div::-webkit-scrollbar {
        width: 5px;
    }

    section[data-testid="stSidebar"] > div::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 10px;
    }
    /* Compact mobile sidebar */
    section[data-testid="stSidebar"] {
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 280px !important;
    }

    /* Compact mobile navigation buttons */
    section[data-testid="stSidebar"] div.stButton > button {
        min-height: 30px !important;
        padding: 0.15rem 0.25rem !important;
        border-radius: 9px !important;
    }

    /* Navigation button text */
    section[data-testid="stSidebar"] div.stButton > button p,
    section[data-testid="stSidebar"] div.stButton > button span {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
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
            font-size: 1.70rem;
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

    st.markdown(
        """
        <div class="sidebar-section-title">
            Navigation
        </div>
        """,
        unsafe_allow_html=True,
    )

    navigation_items = [
        (":material/dashboard:", "Overview"),
        (":material/trending_up:", "Market Trends"),
        (":material/monitor_heart:", "Market Activity"),
        (":material/history:", "Market History"),
        (":material/bar_chart:", "Market Analysis"),
        (":material/description:", "Reports"),
    ]

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Overview"

    for icon, label in navigation_items:

        is_active = st.session_state.current_page == label

        if st.button(
            label,
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            icon=icon,
        ):
            st.session_state.current_page = label
            st.rerun()

    page = st.session_state.current_page

    st.divider()

    st.caption(
        f"Database records: {len(df):,}"
    )


# ============================================================
# PAGE ROUTING
# ============================================================
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