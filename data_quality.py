from modules.ai_engine import generate_ai_response


def generate_data_quality_insights(
    subjects,
    visits,
    queries,
    deviations,
    lab_results
):

    # --------------------------------
    # SUBJECT METRICS
    # --------------------------------

    total_subjects = subjects["Subject_ID"].nunique()

    active_subjects = subjects[
        subjects["Subject_Status"] == "Active"
    ]["Subject_ID"].nunique()

    completed_subjects = subjects[
        subjects["Subject_Status"] == "Completed"
    ]["Subject_ID"].nunique()

    withdrawn_subjects = subjects[
        subjects["Subject_Status"] == "Withdrawn"
    ]["Subject_ID"].nunique()

    screen_failures = subjects[
        subjects["Subject_Status"] == "Screen Failure"
    ]["Subject_ID"].nunique()


    # --------------------------------
    # VISIT METRICS
    # --------------------------------

    total_visits = len(visits)

    completed_visits = len(
        visits[
            visits["Visit_Status"] == "Completed"
        ]
    )

    missed_visits = len(
        visits[
            visits["Missed_Visit"] == "Yes"
        ]
    )


    # --------------------------------
    # QUERY METRICS
    # --------------------------------

    total_queries = len(queries)

    open_queries = len(
        queries[
            queries["Query_Status"] == "Open"
        ]
    )

    resolved_queries = len(
        queries[
            queries["Query_Status"] == "Resolved"
        ]
    )


    # --------------------------------
    # DEVIATION METRICS
    # --------------------------------

    total_deviations = len(deviations)

    open_deviations = len(
        deviations[
            deviations["Deviation_Status"] == "Open"
        ]
    )

    closed_deviations = len(
        deviations[
            deviations["Deviation_Status"] == "Closed"
        ]
    )


    # --------------------------------
    # MISSING DATA ANALYSIS
    # --------------------------------

    subject_missing = subjects.isnull().sum().sum()

    visit_missing = visits.isnull().sum().sum()

    query_missing = queries.isnull().sum().sum()

    deviation_missing = deviations.isnull().sum().sum()

    lab_missing = lab_results.isnull().sum().sum()

    total_missing_values = (
        subject_missing
        + visit_missing
        + query_missing
        + deviation_missing
        + lab_missing
    )


    # --------------------------------
    # SIMPLE DATA QUALITY SCORE
    # --------------------------------

    total_issues = (
        missed_visits
        + open_queries
        + open_deviations
        + total_missing_values
    )

    data_quality_score = max(
        0,
        round(
            (
                (total_subjects - total_issues)
                / total_subjects
            ) * 100,
            2
        )
    )


    # --------------------------------
    # CREATE AI PROMPT
    # --------------------------------

    prompt = f"""
You are ClinicalGenAI, an AI assistant supporting
Clinical Data Management and Clinical Trial Monitoring.

Analyze the following clinical trial data quality metrics.

SUBJECT METRICS:
- Total Subjects: {total_subjects}
- Active Subjects: {active_subjects}
- Completed Subjects: {completed_subjects}
- Withdrawn Subjects: {withdrawn_subjects}
- Screen Failures: {screen_failures}

VISIT METRICS:
- Total Visits: {total_visits}
- Completed Visits: {completed_visits}
- Missed Visits: {missed_visits}

DATA QUERY METRICS:
- Total Queries: {total_queries}
- Open Queries: {open_queries}
- Resolved Queries: {resolved_queries}

PROTOCOL DEVIATION METRICS:
- Total Deviations: {total_deviations}
- Open Deviations: {open_deviations}
- Closed Deviations: {closed_deviations}

DATA COMPLETENESS:
- Total Missing Values: {total_missing_values}

SIMPLIFIED PORTFOLIO DATA QUALITY SCORE:
- Data Quality Score: {data_quality_score}%

Your task:

1. Provide an overall data quality summary.
2. Identify the main areas requiring attention.
3. Highlight operational or data management concerns based only on these metrics.
4. Suggest general monitoring priorities.
5. Keep the response concise and professional.

IMPORTANT RULES:

- Use only the provided metrics.
- Do not invent additional findings.
- Do not provide medical diagnosis or treatment advice.
- Do not claim regulatory compliance.
- The data quality score is a simplified portfolio metric,
  not an official regulatory metric.
- Human review is required for real clinical trial decisions.
"""

    return generate_ai_response(prompt)