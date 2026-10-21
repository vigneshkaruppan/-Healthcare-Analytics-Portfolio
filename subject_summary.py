from modules.ai_engine import generate_ai_response


def generate_subject_summary(
    subject_id,
    subjects,
    visits,
    queries,
    deviations,
    lab_results
):

    # -------------------------
    # SUBJECT INFORMATION
    # -------------------------

    subject = subjects[
        subjects["Subject_ID"] == subject_id
    ]

    if subject.empty:
        return "Subject not found."

    subject_info = subject.iloc[0]

    # -------------------------
    # VISIT INFORMATION
    # -------------------------

    subject_visits = visits[
        visits["Subject_ID"] == subject_id
    ]

    total_visits = len(subject_visits)

    completed_visits = len(
        subject_visits[
            subject_visits["Visit_Status"] == "Completed"
        ]
    )

    missed_visits = len(
        subject_visits[
            subject_visits["Missed_Visit"] == "Yes"
        ]
    )

    # -------------------------
    # QUERY INFORMATION
    # -------------------------

    subject_queries = queries[
        queries["Subject_ID"] == subject_id
    ]

    open_queries = len(
        subject_queries[
            subject_queries["Query_Status"] == "Open"
        ]
    )

    # -------------------------
    # DEVIATION INFORMATION
    # -------------------------

    subject_deviations = deviations[
        deviations["Subject_ID"] == subject_id
    ]

    open_deviations = len(
        subject_deviations[
            subject_deviations["Deviation_Status"] == "Open"
        ]
    )

    # -------------------------
    # LAB RESULTS
    # -------------------------

    subject_labs = lab_results[
        lab_results["Subject_ID"] == subject_id
    ]

    lab_data = subject_labs.to_string(index=False)

    # -------------------------
    # CREATE AI PROMPT
    # -------------------------

    prompt = f"""
Generate a professional clinical trial subject monitoring summary.

Subject Information:
Subject ID: {subject_info['Subject_ID']}
Site ID: {subject_info['Site_ID']}
Age: {subject_info['Age']}
Gender: {subject_info['Gender']}
Subject Status: {subject_info['Subject_Status']}

Visit Information:
Total Visits: {total_visits}
Completed Visits: {completed_visits}
Missed Visits: {missed_visits}

Data Query Information:
Open Queries: {open_queries}

Protocol Deviation Information:
Open Deviations: {open_deviations}

Laboratory Results:
{lab_data}

Generate a concise monitoring summary.

Do not diagnose the subject.
Do not recommend treatment.
Only summarize the provided clinical trial information.
"""

    return generate_ai_response(prompt)