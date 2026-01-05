import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from app.config import PASSING_SCORE
from app.spi import calculate_student_performance_index


def render_student_lookup(df: pd.DataFrame):
    st.header("Student Performance Lookup")

    st.markdown("### Search by ID")

    unique_students = df[["student_id", "student_name"]].drop_duplicates().sort_values("student_id")
    student_ids = unique_students["student_id"].astype(str).tolist()
    options = ["Choose a student..."] + student_ids

    selected = st.selectbox("Select a Student ID", options, index=0, label_visibility="collapsed")

    st.markdown(
        """
        <div class="blue-info-box">
            <span style="margin-right: 10px; font-size: 1.2rem;">ℹ️</span>
            <strong>Select a Student ID to view details.</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if selected == "Choose a student...":
        return

    try:
        student_id = int(selected)
    except ValueError:
        st.error("Please choose a valid student ID.")
        return

    student_data = df[df["student_id"] == student_id]
    if student_data.empty:
        st.warning(f"No student found with ID: {student_id}")
        return

    avg_score = student_data["assessment_score"].mean()
    avg_attendance = student_data["attendance_rate"].mean()
    avg_engagement = student_data["raised_hand_count"].mean()

    student_name = student_data.iloc[0]["student_name"]
    class_level = student_data.iloc[0]["class_level"]
    gender = student_data.iloc[0].get("student_gender", "N/A")

    spi_score, status, status_color, spi_details = calculate_student_performance_index(student_data, PASSING_SCORE)

    courses_perf = student_data.groupby("course_name")["assessment_score"].mean()
    passing_courses = int((courses_perf >= PASSING_SCORE).sum())
    total_courses = int(len(courses_perf))

    avatar_url = f"https://ui-avatars.com/api/?name={student_name}&background=random&size=128"

    st.markdown(
        f"""
        <div style="background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="{avatar_url}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #f0f2f6;">
                    <div>
                        <h2 style="margin: 0; color: #1f1f1f;">{student_name}</h2>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 16px;">ID: {student_id} | Class: {class_level} | {gender}</p>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">SPI Score: {spi_score:.1f}/100</p>
                    </div>
                </div>
                <div style="background-color: {status_color}; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;">
                    {status}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 4px solid #4CAF50;">
                <p style="margin: 0; color: #666; font-size: 14px;">Avg Score</p>
                <h2 style="margin: 5px 0 0 0; color: #4CAF50;">{avg_score:.1f}%</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 4px solid #2196F3;">
                <p style="margin: 0; color: #666; font-size: 14px;">Attendance</p>
                <h2 style="margin: 5px 0 0 0; color: #2196F3;">{avg_attendance:.1f}%</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 4px solid #9C27B0;">
                <p style="margin: 0; color: #666; font-size: 14px;">Engagement</p>
                <h2 style="margin: 5px 0 0 0; color: #9C27B0;">{avg_engagement:.1f}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 4px solid #FF9800;">
                <p style="margin: 0; color: #666; font-size: 14px;">Passing Courses</p>
                <h2 style="margin: 5px 0 0 0; color: #FF9800;">{passing_courses}/{total_courses}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # SPI breakdown
    st.subheader("📊 Student Performance Index (SPI) Breakdown")
    a, b = st.columns(2)

    with a:
        st.markdown(
            f"""
            **Base Components:**
            - Academic (60%): {spi_details['academic_component']:.1f} points
            - Attendance (25%): {spi_details['attendance_component']:.1f} points
            - Engagement (15%): {spi_details['engagement_component']:.1f} points
            - **Base SPI**: {spi_details['base_spi']:.1f} points
            """
        )

    with b:
        st.markdown(
            f"""
            **Penalties Applied:**
            - Failed Courses: -{spi_details['failure_penalty']} points ({spi_details['failed_courses']} course(s))
            - Performance Trend: -{spi_details['trend_penalty']} points ({spi_details['performance_trend']:.1f} point change)
            - **Final SPI**: {spi_score:.1f}/100
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.subheader("📚 Course Breakdown")
        course_perf = student_data.groupby("course_name")["assessment_score"].mean().reset_index()
        course_perf = course_perf.sort_values("assessment_score", ascending=False)

        fig = go.Figure(
            data=[
                go.Bar(
                    x=course_perf["course_name"],
                    y=course_perf["assessment_score"],
                    text=course_perf["assessment_score"].round(1),
                    textposition="outside",
                    textfont=dict(size=12, color="#1f1f1f"),
                    marker_color=["#4CAF50" if s >= PASSING_SCORE else "#EF5350" for s in course_perf["assessment_score"]],
                )
            ]
        )
        fig.add_hline(y=PASSING_SCORE, line_dash="dash", line_color="red", annotation_text="Passing Line")
        fig.update_layout(height=350, showlegend=False, xaxis_title="Course", yaxis_title="Average Score",
                          margin=dict(l=40, r=40, t=40, b=60))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("💡 Automated Insights")

        insights = []

        if status == "EXCELLENT":
            insights.append("✅ **Excellent Performance**: Student is performing exceptionally well across all metrics")
        elif status == "SATISFACTORY":
            insights.append("✅ **Satisfactory Performance**: Student is meeting expectations")
        elif status == "AT RISK":
            insights.append("⚠️ **At Risk**: Student needs support to improve performance")
        else:
            insights.append("🚨 **Critical Status**: Immediate intervention required")

        if avg_score >= 80:
            insights.append("✅ **Strong Academics**: Consistently scoring above 80%")
        elif avg_score >= 70:
            insights.append("✅ **Good Academic Standing**: Maintaining solid grades")
        elif avg_score >= PASSING_SCORE:
            insights.append("⚠️ **Borderline Performance**: Scores just above passing threshold")
        else:
            insights.append(f"🚨 **Academic Emergency**: Failing average (below {PASSING_SCORE})")

        if avg_attendance >= 90:
            insights.append("✅ **Excellent Attendance**: Rarely misses class")
        elif avg_attendance >= 80:
            insights.append("✅ **Good Attendance**: Regular class participation")
        elif avg_attendance >= 70:
            insights.append("⚠️ **Attendance Concern**: Missing classes regularly")
        else:
            insights.append("🚨 **Poor Attendance**: Significant absences affecting performance")

        if spi_details["normalized_engagement"] >= 80:
            insights.append("✅ **Highly Engaged**: Exceptional class participation")
        elif spi_details["normalized_engagement"] >= 50:
            insights.append("✅ **Moderate Engagement**: Participates occasionally")
        else:
            insights.append("⚠️ **Low Engagement**: Rarely participates in class")

        if spi_details["trend_penalty"] > 0:
            insights.append(f"📉 **Declining Trend**: Performance dropped by {abs(spi_details['performance_trend']):.1f} points")
        elif spi_details["performance_trend"] > 10:
            insights.append(f"📈 **Improving Trend**: Performance increased by {spi_details['performance_trend']:.1f} points!")

        if spi_details["failed_courses"] > 0:
            weak = course_perf[course_perf["assessment_score"] < PASSING_SCORE]
            insights.append(f"📚 **Failing {spi_details['failed_courses']} Course(s)**: {', '.join(weak['course_name'].tolist())}")

        strong = course_perf[course_perf["assessment_score"] >= 80]
        if len(strong) > 0:
            insights.append(f"🌟 **Strong Subjects**: {', '.join(strong['course_name'].tolist())}")

        for x in insights:
            st.markdown(x)

        st.markdown("---")
        st.markdown("**📋 Recommendations:**")
        if status == "CRITICAL":
            st.markdown("• **URGENT**: Schedule immediate parent-teacher conference")
            st.markdown("• Develop individualized academic support plan")
            st.markdown("• Consider intensive tutoring services")
            st.markdown("• Investigate barriers to attendance and engagement")
        elif status == "AT RISK":
            st.markdown("• Schedule parent-teacher conference")
            st.markdown("• Provide targeted tutoring for failing courses")
            st.markdown("• Monitor attendance and engagement closely")
        elif status == "SATISFACTORY":
            st.markdown("• Continue current support strategies")
            st.markdown("• Encourage participation in challenging coursework")
        else:
            st.markdown("• Consider advanced placement opportunities")
            st.markdown("• Encourage peer tutoring/mentoring roles")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📄 View Detailed Assessment Records"):
        display = student_data[
            ["course_name", "assessment_no", "assessment_score", "attendance_rate", "raised_hand_count", "moodle_views", "resources_downloads"]
        ].copy()
        display.columns = ["Course", "Assessment #", "Score", "Attendance %", "Hand Raises", "Moodle Views", "Downloads"]
        st.dataframe(display, use_container_width=True)
