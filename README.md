# School Performance Dashboard

A comprehensive student performance evaluation and analytics dashboard built with **Streamlit**. This application provides educators and administrators with actionable insights into student performance, attendance, engagement, and risk assessment.

## Features

### 📊 Overview Tab
- **Key Performance Indicators (KPIs)**: Display overall average scores, pass rate, fail rate, and attendance statistics
- **Score Distribution Analysis**: Visualize assessment score distribution across score ranges (0-40, 40-60, 60-80, 80-100)
- **Class-wise Performance**: Compare average scores across different class levels
- **Assessment Trends**: Track performance metrics by course and class level
- **Course Performance**: Analyze assessment scores by individual courses

### ⚠️ Risk Tab
- **At-Risk Student Identification**: Identify students who are struggling academically
- **Risk Analysis by Class Level**: Visualize the distribution of at-risk students across different class levels
- **Student Performance Index (SPI)**: Calculate comprehensive performance metrics for each student
- **Risk Table**: Detailed list of at-risk students with their metrics

### 🔎 Student Lookup Tab
- **Individual Student Search**: Query student performance by student ID
- **Detailed Performance Metrics**: View comprehensive performance data for a selected student
- **Course-by-Course Analysis**: See assessment scores across all courses
- **Engagement Metrics**: Display student engagement scores based on participation and resource usage
- **Visual Performance Trends**: Charts showing performance patterns and engagement levels

## Project Structure

```
StudentPerformance-Evaluation-tab2-main/
├── main.py                      # Entry point for the Streamlit application
├── requirements.txt             # Python package dependencies
├── Students_Dataset.csv         # Student performance dataset
├── README.md                    # Project documentation
└── app/
    ├── __init__.py
    ├── config.py               # Configuration constants (colors, passing score, etc.)
    ├── data.py                 # Data loading and preprocessing functions
    ├── charts.py               # Plotly chart generation utilities
    ├── styles.py               # CSS styling and theming
    ├── ui.py                   # UI components (KPI cards, headers)
    ├── spi.py                  # Student Performance Index calculations
    └── pages/
        ├── __init__.py
        ├── overview.py         # Overview tab implementation
        ├── risk.py             # Risk analysis tab implementation
        └── student_lookup.py   # Student lookup tab implementation
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudentPerformance-Evaluation-tab2-main
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   - Ensure `Students_Dataset.csv` is in the root directory
   - The CSV should contain the following columns:
     - `student_id`: Unique student identifier
     - `student_name`: Student's name
     - `course_name`: Name of the course
     - `class_level`: Student's class level
     - `assessment_score`: Student's score (0-100)
     - `attendance_rate`: Attendance percentage
     - `raised_hand_count`: Number of times student raised hand
     - `moodle_views`: Number of times student accessed Moodle
     - `resources_downloads`: Number of resources downloaded

## Running the Application

```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

## Dependencies

- **streamlit**: Web application framework for data apps
- **plotly**: Interactive visualization library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing library

## Configuration

Edit `app/config.py` to customize:
- **APP_TITLE**: Application title displayed in the browser
- **PASSING_SCORE**: Minimum score considered as passing (default: 60)
- **PALETTE**: Color scheme for charts and UI components
- **CSV_PATH**: Path to the student dataset

## Key Metrics

### Student Performance Index (SPI)
A comprehensive metric calculated for each student based on:
- Assessment score
- Attendance rate
- Engagement score (combination of participation and resource usage)

### Engagement Score
Calculated as: `raised_hand_count + moodle_views + resources_downloads`

### At-Risk Students
Students identified as at-risk based on their overall performance metrics falling below acceptable thresholds.

## Error Handling

The application includes robust error handling:
- Checks for the presence of `Students_Dataset.csv`
- Validates CSV format and required columns
- Provides user-friendly error messages for common issues

## Performance Notes

- Data is cached using Streamlit's `@st.cache_data` decorator for optimal performance
- The application processes data once at startup and reuses it across tabs

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Changes are tested with sample data
- Documentation is updated accordingly

## License

This project is open source and available for educational use.

## Support

For issues, questions, or suggestions, please refer to the project repository or contact the development team.
