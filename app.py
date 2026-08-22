import streamlit as st
import pandas as pd
from core.io import load_dataset
from core.sql import SQLExecutor

st.set_page_config(page_title="ClarityGrid", page_icon="📊", layout="wide")
st.title("📊 ClarityGrid — Tabular Data Diagnostic Workbench")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Parquet", type=["csv", "parquet"])
if uploaded_file:
    df = load_dataset(uploaded_file)
    t1, t2 = st.tabs(["Data", "SQL Workspace"])
    with t2:
        query = st.text_area("SQL Query", "SELECT * FROM dataset LIMIT 5")
        if st.button("Run Query"):
            executor = SQLExecutor({"dataset": df})
            st.dataframe(executor.execute(query))
