import streamlit as st
from datetime import datetime
from app.config import APP_TITLE


def render_header():
    st.title(APP_TITLE)
    current_year = datetime.now().year
    st.markdown(
        f"**Academic Year {current_year - 1} - {current_year}** • "
        f"Last Updated: {datetime.now().strftime('%B %d, %Y')}"
    )
    st.markdown("---")


def kpi_card(icon: str, label: str, value: str, card_class: str):
    st.markdown(
        f"""
        <div class="kpi-card {card_class}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
