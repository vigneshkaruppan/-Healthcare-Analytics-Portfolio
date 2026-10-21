from modules.ai_engine import generate_ai_response


def generate_deviation_summary(
    deviation_id,
    deviations,
    subjects,
    visits
):

    # -------------------------
    # GET SELECTED DEVIATION
    # -------------------------

    deviation = deviations[
        deviations["Deviation_ID"] == deviation_id
    ]

    if deviation.empty:
        return "Protocol deviation not found."

    deviation_info = deviation.iloc[0]

    subject_id = deviation_info["Subject_ID"]

    # -------------------------
    # GET SUBJECT INFORMATION
    # -------------------------

    subject = subjects[
        subjects["Subject_ID"] == subject_id
    ]

    if subject.empty:

        subject_details = "Subject information not available."

    else:

        subject_info = subject.iloc[0]

        subject_details = f"""
Subject ID: {subject_info['Subject_ID']}
Site ID: {subject_info['Site_ID']}
Age: {subject_info['Age']}
Gender: {subject_info['Gender']}
Subject Status: {subject_info['Subject_Status']}
"""

    # -------------------------
    # GET RELATED VISITS
    # -------------------------

    subject_visits = visits[
        visits["Subject_ID"] == subject_id
    ]

    visit_details = subject_visits.to_string(index=False)

    # -------------------------
    # CREATE AI PROMPT
    # -------------------------

    prompt = f"""
You are an AI assistant supporting Clinical Trial Monitoring
and Clinical Data Management.

Analyze the following protocol deviation.

DEVIATION INFORMATION:

Deviation ID: {deviation_info['Deviation_ID']}
Subject ID: {deviation_info['Subject_ID']}
Deviation Type: {deviation_info['Deviation_Type']}
Description: {deviation_info['Deviation_Description']}
Status: {deviation_info['Deviation_Status']}
Date: {deviation_info['Date']}

SUBJECT INFORMATION:
{subject_details}

RELATED VISIT INFORMATION:
{visit_details}

Your task:

1. Summarize the protocol deviation clearly.
2. Explain the potential data or operational concern based only on the provided information.
3. Generate general monitoring follow-up points.
4. Keep the response concise and professional.

IMPORTANT RULES:

- Use only the provided information.
- Do not invent facts.
- Do not provide medical diagnosis.
- Do not recommend treatment.
- Do not determine patient safety.
- Do not claim regulatory compliance.
- Human clinical and quality review is required.
"""

    return generate_ai_response(prompt)