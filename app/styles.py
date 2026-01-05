import streamlit as st

CSS = """
<style>
    .main > div { padding-top: 1rem; }

    .kpi-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-top: 5px solid #ddd;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .kpi-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1f1f1f; }
    .kpi-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }

    .card-blue { border-top-color: #4A90E2; }
    .card-green { border-top-color: #6BCB77; }
    .card-red { border-top-color: #FF6B6B; }
    .card-orange { border-top-color: #FF8C42; }

    .search-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }

    .blue-info-box {
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        border-radius: 4px;
        color: #0D47A1;
        font-size: 1.1rem;
        margin-top: 1rem;
        display: flex;
        align-items: center;
    }

    h1 { color: #1f1f1f; font-weight: 700; }
    h2, h3 { color: #2c2c2c; font-weight: 600; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
