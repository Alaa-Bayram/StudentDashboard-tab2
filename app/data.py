import streamlit as st
import pandas as pd
from app.config import CSV_PATH, PASSING_SCORE


@st.cache_data
def load_data(path: str = CSV_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in ["student_name", "course_name", "class_level"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["is_passing"] = df["assessment_score"] >= PASSING_SCORE
    df["engagement_score"] = df["raised_hand_count"] + df["moodle_views"] + df["resources_downloads"]

    return df


def compute_overall_metrics(df: pd.DataFrame) -> dict:
    overall_avg = df["assessment_score"].mean()
    pass_rate = (df.groupby("student_id")["is_passing"].mean() * 100).mean()
    fail_rate = 100 - pass_rate
    avg_attendance = df["attendance_rate"].mean()

    return {
        "overall_avg": overall_avg,
        "pass_rate": pass_rate,
        "fail_rate": fail_rate,
        "avg_attendance": avg_attendance,
    }
