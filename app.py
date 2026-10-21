import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LENOVO\\SQLEXPRESS;"
    "DATABASE=ClinicalLIMS_Portfolio;"
    "Trusted_Connection=yes;"
)

query = "SELECT * FROM QC_Control"
df = pd.read_sql(query, conn)
fig, ax = plt.subplots()

df["QC_Result"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")
st.pyplot(fig)

conn.close()