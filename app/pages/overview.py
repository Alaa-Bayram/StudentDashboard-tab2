import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from app.config import PASSING_SCORE, PALETTE
from app.ui import kpi_card
from app.data import compute_overall_metrics
from app.charts import bar_chart


def render_overview(df: pd.DataFrame, show_header: bool = True):
    # show_header kept for flexibility, but main.py already shows global header
    # so here we usually call with show_header=False
    metrics = compute_overall_metrics(df)

    st.header("Performance Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("📈", "Overall Average", f"{metrics['overall_avg']:.1f}", "card-blue")
    with c2:
        kpi_card("👥", "Pass Rate", f"{metrics['pass_rate']:.1f}%", "card-green")
    with c3:
        kpi_card("⚠️", "Fail Rate", f"{metrics['fail_rate']:.1f}%", "card-red")
    with c4:
        kpi_card("📚", "Avg Attendance", f"{metrics['avg_attendance']:.1f}%", "card-orange")

    st.markdown("---")

    # Score Distribution
    st.header("Score Distribution")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Assessment Score Histogram")
        bins = [0, 40, 60, 80, 100]
        labels = ["0-40", "40-60", "60-80", "80-100"]
        tmp = df.copy()
        tmp["score_range"] = pd.cut(tmp["assessment_score"], bins=bins, labels=labels, include_lowest=True)
        dist = tmp["score_range"].value_counts().sort_index()

        fig = bar_chart(
            x=dist.index,
            y=dist.values,
            text=dist.values,
            colors=[PALETTE["red"], "#FFA07A", PALETTE["yellow"], PALETTE["green"]],
            x_title="Score Range",
            y_title="Number of Assessments",
            height=400,
            y_range=[0, max(1, dist.max() * 1.15)],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Class Level Performance Comparison")
        class_perf = df.groupby("class_level")["assessment_score"].mean().reset_index()

        fig = bar_chart(
            x=class_perf["class_level"],
            y=class_perf["assessment_score"],
            text=class_perf["assessment_score"].round(1),
            colors=[PALETTE["blue"], "#50C878", PALETTE["orange"], PALETTE["purple"], PALETTE["yellow"]],
            x_title="Class Level",
            y_title="Average Score",
            height=400,
            y_range=[0, max(1, class_perf["assessment_score"].max() * 1.15)],
        )
        fig.add_hline(y=PASSING_SCORE, line_dash="dash", line_color="red",
                      annotation_text="Passing (60)", annotation_position="right")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Performance by Structure
    st.header("Performance by Structure")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resource Usage by Class Level")
        ru = df.groupby("class_level").agg(
            moodle_views=("moodle_views", "mean"),
            resources_downloads=("resources_downloads", "mean")
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Moodle Views",
            x=ru["class_level"],
            y=ru["moodle_views"],
            marker_color=PALETTE["blue"],
            text=ru["moodle_views"].round(1),
            textposition="inside",
            textfont=dict(size=12, color="white"),
        ))
        fig.add_trace(go.Bar(
            name="Downloads",
            x=ru["class_level"],
            y=ru["resources_downloads"],
            marker_color=PALETTE["orange"],
            text=ru["resources_downloads"].round(1),
            textposition="inside",
            textfont=dict(size=12, color="white"),
        ))
        fig.update_layout(
            barmode="group",
            height=400,
            xaxis_title="Class Level",
            yaxis_title="Average Count",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=60),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Score by Course")
        course_avg = df.groupby("course_name")["assessment_score"].mean().reset_index()
        course_avg = course_avg.sort_values("assessment_score", ascending=False)

        colors = [PALETTE["orange"], "#50C878", PALETTE["purple"], PALETTE["blue"], PALETTE["yellow"]]
        fig = go.Figure(data=[
            go.Pie(
                labels=course_avg["course_name"],
                values=course_avg["assessment_score"],
                marker=dict(colors=colors),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Avg Score: %{value:.1f}<extra></extra>",
            )
        ])
        fig.update_layout(height=400, margin=dict(l=40, r=40, t=40, b=40))
        st.plotly_chart(fig, use_container_width=True)
