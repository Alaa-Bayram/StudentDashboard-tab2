import streamlit as st

from app.config import APP_TITLE
from app.styles import inject_css
from app.data import load_data, preprocess
from app.ui import render_header
from app.pages.overview import render_overview
from app.pages.risk import render_risk
from app.pages.student_lookup import render_student_lookup


def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="collapsed")
    inject_css()

    # Load + prepare data once
    df = load_data()
    df = preprocess(df)

    # Global header
    render_header()
    
    # Tabs navigation
    tab_overview, tab_risk, tab_lookup = st.tabs(["📊 Overview", "⚠️ Risk", "🔎 Student Lookup"])

    with tab_overview:
        render_overview(df, show_header=False)

    with tab_risk:
        render_risk(df)

    with tab_lookup:
        render_student_lookup(df)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        st.error("⚠️ Error: 'Students_Dataset.csv' not found. Put it next to main.py.")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
        st.info("Please check that your CSV file is properly formatted and contains the required columns.")
