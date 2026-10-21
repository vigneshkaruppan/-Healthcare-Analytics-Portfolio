from modules.ai_engine import generate_ai_response


def generate_monitoring_report(
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

    active_subjects = len(
        subjects[
            subjects["Subject_Status"] == "Active"
        ]
    )

    completed_subjects = len(
        subjects[
            subjects["Subject_Status"] == "Completed"
        ]
    )

    withdrawn_subjects = len(
        subjects[
            subjects["Subject_Status"] == "Withdrawn"
        ]
    )

    screen_failures = len(
        subjects[
            subjects["Subject_Status"] == "Screen Failure"
        ]
    )


    # --------------------------------
    # SITE METRICS
    # --------------------------------

    total_sites = subjects["Site_ID"].nunique()

    site_subject_counts = (
        subjects.groupby("Site_ID")["Subject_ID"]
        .nunique()
        .to_dict()
    )


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
    # LAB DATA METRICS
    # --------------------------------

    total_lab_records = len(lab_results)

    missing_lab_values = (
        lab_results.isnull().sum().sum()
    )


    # --------------------------------
    # DATA QUALITY METRIC
    # --------------------------------

    total_missing_values = (
        subjects.isnull().sum().sum()
        + visits.isnull().sum().sum()
        + queries.isnull().sum().sum()
        + deviations.isnull().sum().sum()
        + lab_results.isnull().sum().sum()
    )

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
                total_subjects - total_issues
            )
            / total_subjects
            * 100,
            2
        )
    )


    # --------------------------------
    # CREATE AI PROMPT
    # --------------------------------

    prompt = f"""
You are ClinicalGenAI, an AI assistant supporting
Clinical Trial Monitoring and Clinical Data Management.

Generate a concise and professional Clinical Trial
Monitoring Summary based ONLY on the provided metrics.

STUDY OVERVIEW:

Total Subjects: {total_subjects}
Active Subjects: {active_subjects}
Completed Subjects: {completed_subjects}
Withdrawn Subjects: {withdrawn_subjects}
Screen Failures: {screen_failures}

SITE INFORMATION:

Total Sites: {total_sites}
Subjects per Site: {site_subject_counts}

VISIT MONITORING:

Total Visits: {total_visits}
Completed Visits: {completed_visits}
Missed Visits: {missed_visits}

DATA QUERY MONITORING:

Total Queries: {total_queries}
Open Queries: {open_queries}
Resolved Queries: {resolved_queries}

PROTOCOL DEVIATION MONITORING:

Total Deviations: {total_deviations}
Open Deviations: {open_deviations}
Closed Deviations: {closed_deviations}

LABORATORY DATA:

Total Lab Records: {total_lab_records}
Missing Lab Values: {missing_lab_values}

SIMPLIFIED DATA QUALITY INDICATOR:

Data Quality Score: {data_quality_score}%

Generate the report using the following sections:

1. Executive Summary
2. Subject Enrollment and Status
3. Visit Monitoring
4. Data Query Status
5. Protocol Deviation Status
6. Data Quality Overview
7. Key Monitoring Priorities

IMPORTANT RULES:

- Use only the provided metrics.
- Do not invent information.
- Do not provide medical diagnosis.
- Do not make regulatory compliance claims.
- Do not state that issues are resolved unless indicated.
- The data quality score is a simplified portfolio metric.
- This report requires human review before any real-world use.
"""

    return generate_ai_response(prompt)