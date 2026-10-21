import streamlit as st
import pandas as pd
import plotly.express as px

from modules.risk_engine import calculate_study_risk


def show_dashboard(subjects, visits, queries, deviations, lab_results):

    st.title("📊 Clinical Trial Monitoring Dashboard")

    st.caption(
        "Real-time study monitoring and operational data quality overview"
    )

    # ==================================
    # SITE FILTER
    # ==================================

    st.sidebar.subheader("🏥 Study Filters")

    available_sites = subjects["Site_ID"].unique()

    selected_sites = st.sidebar.multiselect(
        "Select Site",
        options=available_sites,
        default=available_sites
    )

    # Filter Subjects

    filtered_subjects = subjects[
        subjects["Site_ID"].isin(selected_sites)
    ]

    selected_subject_ids = filtered_subjects["Subject_ID"].unique()

    # Filter Related Tables

    filtered_visits = visits[
        visits["Subject_ID"].isin(selected_subject_ids)
    ]

    filtered_queries = queries[
        queries["Subject_ID"].isin(selected_subject_ids)
    ]

    filtered_deviations = deviations[
        deviations["Subject_ID"].isin(selected_subject_ids)
    ]

    filtered_lab_results = lab_results[
        lab_results["Subject_ID"].isin(selected_subject_ids)
    ]

    # ==================================
    # KPI CALCULATIONS
    # ==================================

    total_subjects = (
        filtered_subjects["Subject_ID"].nunique()
    )

    active_subjects = (
        filtered_subjects[
            filtered_subjects["Subject_Status"] == "Active"
        ]["Subject_ID"].nunique()
    )

    missed_visits = len(
        filtered_visits[
            filtered_visits["Missed_Visit"] == "Yes"
        ]
    )

    open_queries = len(
        filtered_queries[
            filtered_queries["Query_Status"] == "Open"
        ]
    )

    open_deviations = len(
        filtered_deviations[
            filtered_deviations["Deviation_Status"] == "Open"
        ]
    )

    # ==================================
    # DATA QUALITY SCORE
    # ==================================

    total_issues = (
        missed_visits
        + open_queries
        + open_deviations
    )

    if total_subjects > 0:

        data_quality = max(
            0,
            round(
                (
                    (total_subjects - total_issues)
                    / total_subjects
                ) * 100,
                2
            )
        )

    else:

        data_quality = 0

    # ==================================
    # RISK CALCULATION
    # ==================================

    risk_data = calculate_study_risk(
        filtered_subjects,
        filtered_visits,
        filtered_queries,
        filtered_deviations
    )

    # ==================================
    # KPI CARDS
    # ==================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Total Subjects",
        total_subjects
    )

    col2.metric(
        "🟢 Active Subjects",
        active_subjects
    )

    col3.metric(
        "❓ Open Queries",
        open_queries
    )

    col4.metric(
        "⚠️ Open Deviations",
        open_deviations
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "📅 Missed Visits",
        missed_visits
    )

    col6.metric(
        "📈 Data Quality",
        f"{data_quality}%"
    )

    col7.metric(
        "🚨 Study Risk",
        risk_data["risk_level"]
    )

    st.divider()

    # ==================================
    # RISK ALERT
    # ==================================

    st.subheader("🚨 Study Risk Status")

    if risk_data["risk_level"] == "High":

        st.error(
            f"HIGH RISK: Risk Score {risk_data['risk_score']} "
            "- Immediate monitoring attention recommended."
        )

    elif risk_data["risk_level"] == "Medium":

        st.warning(
            f"MEDIUM RISK: Risk Score {risk_data['risk_score']} "
            "- Increased monitoring may be required."
        )

    else:

        st.success(
            f"LOW RISK: Risk Score {risk_data['risk_score']} "
            "- Current operational risk appears manageable."
        )

    # ==================================
    # CHARTS
    # ==================================

    col1, col2 = st.columns(2)

    # SUBJECT STATUS

    with col1:

        st.subheader("👥 Subject Status")

        status_counts = (
            filtered_subjects["Subject_Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Subject Status",
            "Count"
        ]

        fig_status = px.bar(
            status_counts,
            x="Subject Status",
            y="Count",
            text="Count",
            title="Subjects by Status"
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    # VISIT STATUS

    with col2:

        st.subheader("📅 Visit Status")

        visit_counts = (
            filtered_visits["Visit_Status"]
            .value_counts()
            .reset_index()
        )

        visit_counts.columns = [
            "Visit Status",
            "Count"
        ]

        fig_visit = px.pie(
            visit_counts,
            names="Visit Status",
            values="Count",
            title="Visit Completion Status"
        )

        st.plotly_chart(
            fig_visit,
            use_container_width=True
        )

    # ==================================
    # QUERY STATUS
    # ==================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("❓ Query Status")

        query_counts = (
            filtered_queries["Query_Status"]
            .value_counts()
            .reset_index()
        )

        query_counts.columns = [
            "Query Status",
            "Count"
        ]

        fig_query = px.bar(
            query_counts,
            x="Query Status",
            y="Count",
            text="Count",
            title="Data Query Status"
        )

        st.plotly_chart(
            fig_query,
            use_container_width=True
        )

    # DEVIATION STATUS

    with col2:

        st.subheader("⚠️ Deviation Status")

        deviation_counts = (
            filtered_deviations["Deviation_Status"]
            .value_counts()
            .reset_index()
        )

        deviation_counts.columns = [
            "Deviation Status",
            "Count"
        ]

        fig_deviation = px.pie(
            deviation_counts,
            names="Deviation Status",
            values="Count",
            title="Protocol Deviation Status"
        )

        st.plotly_chart(
            fig_deviation,
            use_container_width=True
        )

    st.divider()

    # ==================================
    # OPEN ISSUES TABLES
    # ==================================

    st.subheader("❗ Open Data Queries")

    open_query_data = filtered_queries[
        filtered_queries["Query_Status"] == "Open"
    ]

    st.dataframe(
        open_query_data,
        use_container_width=True
    )

    st.subheader("⚠️ Open Protocol Deviations")

    open_deviation_data = filtered_deviations[
        filtered_deviations["Deviation_Status"] == "Open"
    ]

    st.dataframe(
        open_deviation_data,
        use_container_width=True
    )