from modules.ai_engine import generate_ai_response


def generate_query_analysis(query_id, queries, subjects):

    # Get selected query
    query = queries[
        queries["Query_ID"] == query_id
    ]

    if query.empty:
        return "Query not found."

    query_info = query.iloc[0]

    # Get subject information
    subject_id = query_info["Subject_ID"]

    subject = subjects[
        subjects["Subject_ID"] == subject_id
    ]

    # Check if subject exists
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

    # Create structured AI prompt
    prompt = f"""
You are a Clinical Data Management assistant.

Analyze the following clinical trial data query.

QUERY INFORMATION:

Query ID: {query_info['Query_ID']}
Subject ID: {query_info['Subject_ID']}
Query Category: {query_info['Query_Category']}
Query Description: {query_info['Query_Description']}
Query Status: {query_info['Query_Status']}
Created Date: {query_info['Created_Date']}

SUBJECT INFORMATION:
{subject_details}

Your task:

1. Summarize the data issue.
2. Explain why the issue requires review.
3. Suggest general clinical data management follow-up actions.
4. Keep the response concise and professional.

IMPORTANT:
- Use only the provided information.
- Do not invent patient information.
- Do not provide medical diagnosis.
- Do not recommend treatment.
- Do not claim the data has been corrected.
- Clearly distinguish between facts and suggested follow-up.
"""

    return generate_ai_response(prompt)