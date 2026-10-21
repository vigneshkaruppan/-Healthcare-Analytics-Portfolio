import ollama


def generate_ai_response(prompt):

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": """
You are ClinicalGenAI, an AI assistant for Clinical Trials
and Clinical Data Management.

Your responsibilities include:
- Summarizing clinical trial data
- Explaining data quality issues
- Summarizing subject information
- Assisting with query and deviation summaries

IMPORTANT RULES:
- Use only the information provided in the prompt.
- Do not invent missing information.
- Do not provide medical diagnosis.
- Do not provide treatment recommendations.
- Keep responses professional and concise.
- Clearly state when information is unavailable.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"AI Engine Error: {str(e)}"