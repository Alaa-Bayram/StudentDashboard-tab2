import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from app.config import PASSING_SCORE, PALETTE
from app.spi import build_student_spi_table, calculate_student_performance_index
from app.charts import bar_chart


def render_risk(df: pd.DataFrame):
    student_avg = build_student_spi_table(df)

    st.header("Risk Overview")
    col1, col2 = st.columns(2)

    at_risk_by_class = (
        student_avg[student_avg["at_risk"]]
        .groupby("class_level")
        .size()
        .reset_index(name="count")
    )
    at_risk_total = int(student_avg["at_risk"].sum())

    with col1:
        st.subheader("At-Risk Students by Class Level")
        if len(at_risk_by_class) > 0:
            fig = bar_chart(
                x=at_risk_by_class["class_level"],
                y=at_risk_by_class["count"],
                text=at_risk_by_class["count"],
                colors=PALETTE["red"],
                height=350,
                y_range=[0, max(1, at_risk_by_class["count"].max() * 1.15)],
                x_title="Class Level",
                y_title="Students at Risk",
            )
        else:
            fig = bar_chart(x=[], y=[], height=350, y_range=[0, 10], x_title="Class Level", y_title="Students at Risk")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Overall Student Status")
        status_counts = student_avg["status"].value_counts()
        order = ["EXCELLENT", "SATISFACTORY", "AT RISK", "CRITICAL"]
        labels = [s for s in order if s in status_counts.index]
        values = [int(status_counts[s]) for s in labels]
        colors_map = {
            "EXCELLENT": PALETTE["dark_green"],
            "SATISFACTORY": PALETTE["amber"],
            "AT RISK": PALETTE["deep_orange"],
            "CRITICAL": PALETTE["dark_red"],
        }
        colors = [colors_map[s] for s in labels]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors),
                                     hole=0.5, textinfo="label+value+percent")])
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # At-Risk Students Analysis
    st.header("⚠️ At-Risk Students Analysis")

    class_levels = sorted(student_avg["class_level"].unique())
    tabs = st.tabs([f"C {cl.replace('C', '')}" for cl in class_levels])

    for i, cl in enumerate(class_levels):
        with tabs[i]:
            at_risk_students = student_avg[(student_avg["class_level"] == cl) & (student_avg["at_risk"])].sort_values("spi_score")

            st.markdown(f"### C {cl.replace('C', '')} ({len(at_risk_students)} at risk)")

            if len(at_risk_students) == 0:
                st.success(f"No at-risk students in C {cl.replace('C', '')}")
                continue

            st.markdown("**Students classified as AT RISK or CRITICAL based on SPI:**")
            st.markdown("- SPI < 65 (academics + attendance + engagement + failures + trends)")
            st.markdown("")

            for _, student in at_risk_students.iterrows():
                status_emoji = "🔴" if student["status"] == "CRITICAL" else "⚠️"
                with st.expander(f"{status_emoji} {student['student_name']} - SPI: {student['spi_score']:.1f} ({student['status']})"):
                    a, b, c = st.columns(3)
                    with a:
                        st.markdown("**Avg Score**")
                        st.markdown(f"{student['assessment_score']:.1f}")
                    with b:
                        st.markdown("**Attendance**")
                        st.markdown(f"{student['attendance_rate']:.1f}%")
                    with c:
                        st.markdown("**Engagement**")
                        st.markdown(f"{student['raised_hand_count']:.0f}")

                    sdata = df[df["student_id"] == student["student_id"]]
                    _, _, _, details = calculate_student_performance_index(sdata, PASSING_SCORE)

                    st.markdown("**Contributing Factors:**")
                    if student["assessment_score"] < PASSING_SCORE:
                        st.markdown(f"- Failing average (below {PASSING_SCORE})")
                    if student["attendance_rate"] < 70:
                        st.markdown("- Low attendance")
                    if student["raised_hand_count"] < 10:
                        st.markdown("- Minimal engagement")
                    if details["failed_courses"] > 0:
                        st.markdown(f"- Failing {details['failed_courses']} course(s)")
                    if details["trend_penalty"] > 0:
                        st.markdown(f"- Declining trend ({details['performance_trend']:.1f} point drop)")

    st.markdown("---")

    # Priority Actions
    st.error("### ⚠️ Priority Actions Required")
    st.markdown(f"• **{at_risk_total} students** are currently at risk (AT RISK or CRITICAL status)")

    critical = student_avg[student_avg["status"] == "CRITICAL"]
    if len(critical) > 0:
        st.markdown(f"• **{len(critical)} students in CRITICAL status** require immediate intervention")

    st.markdown("• Schedule parent-teacher conferences for students with multiple risk factors")
    st.markdown("• Consider tutoring programs for students with critically low grades")
    st.markdown("• Address attendance barriers through counseling or family support services")
    st.markdown("• Implement engagement strategies for students showing minimal participation")

    st.markdown("---")
