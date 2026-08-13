import streamlit as st
import pandas as pd
from core.io import load_dataset
from core.profiling import profile_dataset

st.set_page_config(page_title="ClarityGrid", page_icon="📊", layout="wide")
st.title("📊 ClarityGrid — Tabular Data Diagnostic Workbench")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Parquet", type=["csv", "parquet"])
if uploaded_file:
    df = load_dataset(uploaded_file)
    profile = profile_dataset(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", f"{profile.row_count:,}")
    col2.metric("Total Columns", profile.col_count)
    col3.metric("Memory Footprint", f"{profile.memory_bytes / (1024*1024):.2f} MB")
    
    st.subheader("Data Preview")
    st.dataframe(df.head(10))
