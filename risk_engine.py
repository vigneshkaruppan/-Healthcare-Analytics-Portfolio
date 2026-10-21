def calculate_study_risk(subjects, visits, queries, deviations):

    # --------------------------------
    # CALCULATE RISK METRICS
    # --------------------------------

    missed_visits = len(
        visits[visits["Missed_Visit"] == "Yes"]
    )

    open_queries = len(
        queries[queries["Query_Status"] == "Open"]
    )

    open_deviations = len(
        deviations[deviations["Deviation_Status"] == "Open"]
    )

    total_subjects = subjects["Subject_ID"].nunique()

    # --------------------------------
    # RISK SCORE
    # --------------------------------

    risk_score = (
        missed_visits * 3
        + open_queries * 2
        + open_deviations * 4
    )

    # Normalize Score

    if total_subjects > 0:

        normalized_score = round(
            (risk_score / total_subjects) * 10,
            2
        )

    else:

        normalized_score = 0

    # --------------------------------
    # RISK CATEGORY
    # --------------------------------

    if normalized_score < 3:

        risk_level = "Low"

    elif normalized_score < 6:

        risk_level = "Medium"

    else:

        risk_level = "High"

    # --------------------------------
    # RETURN RESULTS
    # --------------------------------

    return {
        "risk_score": normalized_score,
        "risk_level": risk_level,
        "missed_visits": missed_visits,
        "open_queries": open_queries,
        "open_deviations": open_deviations
    }