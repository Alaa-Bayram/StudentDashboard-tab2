import pandas as pd
from app.config import PASSING_SCORE, PALETTE


def calculate_student_performance_index(student_data: pd.DataFrame, passing_score: int = PASSING_SCORE):
    # Academic (60%)
    avg_score = student_data["assessment_score"].mean()
    academic_component = avg_score * 0.60

    # Attendance (25%)
    avg_attendance = student_data["attendance_rate"].mean()
    attendance_component = avg_attendance * 0.25

    # Engagement (15%) based on raised hands, normalized to 30
    avg_engagement = student_data["raised_hand_count"].mean()
    normalized_engagement = min((avg_engagement / 30) * 100, 100)
    engagement_component = normalized_engagement * 0.15

    base_spi = academic_component + attendance_component + engagement_component

    # Penalty: failed courses
    courses_perf = student_data.groupby("course_name")["assessment_score"].mean()
    failed_courses = int((courses_perf < passing_score).sum())

    if failed_courses == 1:
        failure_penalty = 5
    elif failed_courses >= 2:
        failure_penalty = 10
    else:
        failure_penalty = 0

    # Penalty: declining trend
    assessment_scores = student_data.groupby("assessment_no")["assessment_score"].mean()
    trend_penalty = 0
    performance_change = 0.0

    if len(assessment_scores) >= 2:
        first_avg = float(assessment_scores.iloc[0])
        last_avg = float(assessment_scores.iloc[-1])
        performance_change = last_avg - first_avg

        if performance_change < -10:
            trend_penalty = 5

    spi_score = base_spi - failure_penalty - trend_penalty
    spi_score = max(0, min(100, spi_score))

    # Status
    if spi_score >= 80:
        status, color = "EXCELLENT", PALETTE["dark_green"]
    elif spi_score >= 65:
        status, color = "SATISFACTORY", PALETTE["amber"]
    elif spi_score >= 50:
        status, color = "AT RISK", PALETTE["deep_orange"]
    else:
        status, color = "CRITICAL", PALETTE["dark_red"]

    details = {
        "base_spi": base_spi,
        "academic_component": academic_component,
        "attendance_component": attendance_component,
        "engagement_component": engagement_component,
        "failure_penalty": failure_penalty,
        "trend_penalty": trend_penalty,
        "failed_courses": failed_courses,
        "performance_trend": performance_change,
        "normalized_engagement": normalized_engagement,
    }
    return spi_score, status, color, details


def build_student_spi_table(df: pd.DataFrame) -> pd.DataFrame:
    student_avg = (
        df.groupby("student_id")
        .agg(
            assessment_score=("assessment_score", "mean"),
            attendance_rate=("attendance_rate", "mean"),
            raised_hand_count=("raised_hand_count", "mean"),
            class_level=("class_level", "first"),
            student_name=("student_name", "first"),
        )
        .reset_index()
    )

    spi_rows = []
    for sid in student_avg["student_id"]:
        sdata = df[df["student_id"] == sid]
        spi_score, status, status_color, _ = calculate_student_performance_index(sdata, PASSING_SCORE)
        spi_rows.append(
            {"student_id": sid, "spi_score": spi_score, "status": status, "status_color": status_color}
        )

    spi_df = pd.DataFrame(spi_rows)
    student_avg = student_avg.merge(spi_df, on="student_id", how="left")
    student_avg["at_risk"] = student_avg["status"].isin(["AT RISK", "CRITICAL"])
    return student_avg
