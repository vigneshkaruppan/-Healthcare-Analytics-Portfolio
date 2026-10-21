import streamlit as st
from modules.subject_summary import generate_subject_summary
from modules.data_loader import load_data
from modules.dashboard import show_dashboard
from modules.ai_engine import generate_ai_response
from modules.query_assistant import generate_query_analysis
from modules.deviation_summary import generate_deviation_summary
from modules.data_quality import generate_data_quality_insights
from modules.monitoring_report import generate_monitoring_report
from modules.risk_engine import calculate_study_risk
from modules.ai_risk_assistant import generate_risk_recommendations
from modules.ui import apply_custom_css
from rag.rag_engine import ask_clinical_rag
from modules.report_export import create_pdf_report

apply_custom_css()
st.set_page_config(
    page_title="ClinicalGenAI",
    page_icon="🤖",
    layout="wide"
)
# ------------------------------------------
# Protocol RAG Assistant
# ------------------------------------------

st.subheader("📚 Clinical Protocol RAG Assistant")

st.write(
    "Ask questions about your clinical trial protocol. "
    "The assistant retrieves relevant document content "
    "and uses Llama 3.2 to generate an answer."
)

question = st.text_input(
    "Enter your clinical question:",
    placeholder="What are the inclusion criteria?"
)
if st.button("Generate RAG Answer"):
    if question.strip():
        with st.spinner("Searching the protocol and generating an answer..."):
            try:
                result = ask_clinical_rag(question)

                st.markdown("### 🤖 Generative AI Answer")
                st.write(result["answer"])

                st.markdown("### 📂 Retrieved Protocol Sources")

                if result["sources"]:
                    for source in result["sources"]:
                        st.markdown(
                            f"**Document:** {source['document']}"
                        )

                        st.markdown(
                            f"**Chunk ID:** {source['chunk_id']}"
                        )

                        with st.expander("View supporting protocol text"):
                            st.write(source["text"])

                else:
                    st.info("No supporting document sources were retrieved.")

            except Exception as e:
                st.error(f"RAG Error: {e}")
    else:
        st.warning("Please enter a clinical question.")
st.subheader("📚 ClinicalGenAI Knowledge Assistant")

question = st.text_input(
    "Ask a question about clinical trial documents:",
    key="clinical_rag_question"
)

if st.button("Generate Answer", key="clinical_rag_button"):

    if question.strip():

        with st.spinner("Searching clinical documents..."):

            result = ask_clinical_rag(question)

        st.markdown("### 🤖 Generative AI Answer")
        st.write(result["answer"])

        st.markdown("### 📄 Source Documents")

        for source in result["sources"]:

            page = source["page"]

            if page is not None:
                location = f"Page {page}"
            else:
                location = "Text document"

            st.markdown(
                f"**Document:** {source['document']}  \n"
                f"**Location:** {location}  \n"
                f"**Chunk:** {source['chunk_id']}"
            )

            with st.expander("View source text"):
                st.write(source["text"])

    else:
        st.warning("Please enter a question.")        
        
        






# LOGIN SIMULATION
# --------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def login():

    st.title("🔐 ClinicalGenAI Login")

    st.write(
        "Clinical Trial Analytics & Generative AI Platform"
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "clinical123":

            st.session_state.authenticated = True

            st.success("Login successful!")

            st.rerun()

        else:

            st.error("Invalid username or password.")


if not st.session_state.authenticated:

    login()

    st.stop()

# Load Data
subjects,visits,queries,deviations,lab_results = load_data()

# Sidebar
st.sidebar.title("🤖 ClinicalGenAI")
st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.authenticated = False

    st.rerun()

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "👤 Subject AI Summary",
        "❓ Query AI Assistant",
        "⚠️ Deviation AI Summary",
        "📈 Data Quality AI",
        "🚨 AI Risk Analysis",
        "📄 Monitoring Report"
    ]
)


# Dashboard Page
if page == "📊 Dashboard":

    show_dashboard(
        subjects,
        visits,
        queries,
        deviations,
        lab_results
    )


# Placeholder pages
elif page == "👤 Subject AI Summary":

    st.title("🤖 AI Subject Clinical Summary")

    st.write(
        "Select a clinical trial subject and generate an AI-powered monitoring summary."
    )

    subject_id = st.selectbox(
        "Select Subject ID",
        subjects["Subject_ID"].unique()
    )

    if st.button("🤖 Generate AI Summary"):

        with st.spinner("ClinicalGenAI is analyzing subject data..."):

            summary = generate_subject_summary(
                subject_id,
                subjects,
                visits,
                queries,
                deviations,
                lab_results
            )

        st.subheader("AI Generated Clinical Monitoring Summary")

        st.write(summary)

elif page == "❓ Query AI Assistant":

    st.title("❓ AI Clinical Data Query Assistant")

    st.write(
        "Select a clinical data query and generate an AI-powered analysis."
    )

    query_id = st.selectbox(
        "Select Query ID",
        queries["Query_ID"].unique()
    )

    # Display selected query information
    selected_query = queries[
        queries["Query_ID"] == query_id
    ]

    st.subheader("Selected Query Information")
    st.dataframe(
        selected_query,
        use_container_width=True
    )

    # Generate AI analysis
    if st.button("🤖 Analyze Query with AI"):

        with st.spinner(
            "ClinicalGenAI is analyzing the data query..."
        ):

            analysis = generate_query_analysis(
                query_id,
                queries,
                subjects
            )

        st.subheader("🤖 AI Query Analysis")

        st.write(analysis)


elif page == "⚠️ Deviation AI Summary":

    st.title("⚠️ AI Protocol Deviation Summary")

    st.write(
        "Select a protocol deviation and generate an AI-powered monitoring summary."
    )

    deviation_id = st.selectbox(
        "Select Deviation ID",
        deviations["Deviation_ID"].unique()
    )

    # Display selected deviation
    selected_deviation = deviations[
        deviations["Deviation_ID"] == deviation_id
    ]

    st.subheader("Selected Protocol Deviation")

    st.dataframe(
        selected_deviation,
        use_container_width=True
    )

    # Generate AI summary
    if st.button("🤖 Generate AI Deviation Summary"):

        with st.spinner(
            "ClinicalGenAI is analyzing the protocol deviation..."
        ):

            summary = generate_deviation_summary(
                deviation_id,
                deviations,
                subjects,
                visits
            )

        st.subheader("🤖 AI Generated Deviation Summary")

        st.write(summary)

elif page == "📈 Data Quality AI":

    st.title("📈 AI Clinical Data Quality Insights")

    st.write(
        "Analyze overall clinical trial data quality using Generative AI."
    )

    # -------------------------
    # Calculate Quick Metrics
    # -------------------------

    total_subjects = subjects["Subject_ID"].nunique()

    missed_visits = len(
        visits[
            visits["Missed_Visit"] == "Yes"
        ]
    )

    open_queries = len(
        queries[
            queries["Query_Status"] == "Open"
        ]
    )

    open_deviations = len(
        deviations[
            deviations["Deviation_Status"] == "Open"
        ]
    )

    missing_values = (
        subjects.isnull().sum().sum()
        + visits.isnull().sum().sum()
        + queries.isnull().sum().sum()
        + deviations.isnull().sum().sum()
        + lab_results.isnull().sum().sum()
    )

    # -------------------------
    # Display KPI Cards
    # -------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("👥 Subjects", total_subjects)
    col2.metric("📅 Missed Visits", missed_visits)
    col3.metric("❓ Open Queries", open_queries)
    col4.metric("⚠️ Open Deviations", open_deviations)
    col5.metric("📂 Missing Values", missing_values)

    st.divider()

    # -------------------------
    # Generate AI Insights
    # -------------------------

    if st.button("🤖 Generate AI Data Quality Insights"):

        with st.spinner(
            "ClinicalGenAI is analyzing clinical trial data quality..."
        ):

            insights = generate_data_quality_insights(
                subjects,
                visits,
                queries,
                deviations,
                lab_results
            )

        st.subheader("🤖 AI Generated Data Quality Insights")

        st.write(insights)
elif page == "🚨 AI Risk Analysis":

    st.title("🚨 AI Clinical Trial Risk Analysis")

    st.write(
        "Analyze operational study risks using clinical trial metrics "
        "and Generative AI."
    )

    # Calculate Risk

    risk_data = calculate_study_risk(
        subjects,
        visits,
        queries,
        deviations
    )

    # Risk KPIs

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📅 Missed Visits",
        risk_data["missed_visits"]
    )

    col2.metric(
        "❓ Open Queries",
        risk_data["open_queries"]
    )

    col3.metric(
        "⚠️ Open Deviations",
        risk_data["open_deviations"]
    )

    col4.metric(
        "🚨 Risk Level",
        risk_data["risk_level"]
    )

    st.divider()

    # Risk Status

    if risk_data["risk_level"] == "High":

        st.error(
            f"High Risk Study Status | "
            f"Risk Score: {risk_data['risk_score']}"
        )

    elif risk_data["risk_level"] == "Medium":

        st.warning(
            f"Medium Risk Study Status | "
            f"Risk Score: {risk_data['risk_score']}"
        )

    else:

        st.success(
            f"Low Risk Study Status | "
            f"Risk Score: {risk_data['risk_score']}"
        )

    # AI Analysis

    if st.button("🤖 Generate AI Risk Recommendations"):

        with st.spinner(
            "ClinicalGenAI is analyzing study risks..."
        ):

            recommendations = generate_risk_recommendations(
                risk_data
            )

        st.subheader("🤖 AI Risk Analysis")

        st.markdown(recommendations)
elif page == "📄 Monitoring Report":

    st.title("📄 AI Clinical Monitoring Report")

    st.write(
        "Generate an AI-powered clinical trial monitoring summary "
        "using the available study data."
    )

    # --------------------------------
    # Quick Study Overview
    # --------------------------------

    total_subjects = subjects["Subject_ID"].nunique()

    total_sites = subjects["Site_ID"].nunique()

    open_queries = len(
        queries[
            queries["Query_Status"] == "Open"
        ]
    )

    open_deviations = len(
        deviations[
            deviations["Deviation_Status"] == "Open"
        ]
    )

    # KPI Cards

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Total Subjects", total_subjects)
    col2.metric("🏥 Total Sites", total_sites)
    col3.metric("❓ Open Queries", open_queries)
    col4.metric("⚠️ Open Deviations", open_deviations)

    st.divider()

    # --------------------------------
    # Generate Report
    # --------------------------------

    if st.button("🤖 Generate AI Monitoring Report"):

        with st.spinner(
            "ClinicalGenAI is generating the monitoring report..."):
        

            report = generate_monitoring_report(
                subjects,
                visits,
                queries,
                deviations,
                lab_results
            )

        st.subheader("🤖 AI Generated Clinical Monitoring Report")
        st.markdown(report)
        pdf_path = create_pdf_report(report)

with open(pdf_path, "rb") as pdf_file:

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="ClinicalGenAI_Monitoring_Report.pdf",
        mime="application/pdf"
    )

        

       

