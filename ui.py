import streamlit as st


def apply_custom_css():

    st.markdown(
        """
        <style>

        .main {
            background-color: #f8f9fa;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1 {
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #e6e6e6;
        }

        </style>
        """,
        unsafe_allow_html=True
    )