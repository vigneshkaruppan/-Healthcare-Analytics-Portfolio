from modules.ai_engine import generate_ai_response


def generate_risk_recommendations(risk_data):

    prompt = f"""
You are an AI assistant supporting Clinical Trial Monitoring.

Analyze the following study risk metrics.

RISK METRICS:

Risk Score: {risk_data['risk_score']}

Risk Level: {risk_data['risk_level']}

Missed Visits: {risk_data['missed_visits']}

Open Data Queries: {risk_data['open_queries']}

Open Protocol Deviations: {risk_data['open_deviations']}


Your task:

1. Explain the overall study operational risk.
2. Identify the most important monitoring concerns.
3. Suggest general monitoring priorities.
4. Rank priorities from highest to lowest.

IMPORTANT:

- Use only the provided metrics.
- Do not invent information.
- Do not make medical decisions.
- Do not provide treatment recommendations.
- Do not claim regulatory compliance.
- This is a simplified portfolio risk model.
- Human review is required.
"""

    return generate_ai_response(prompt)