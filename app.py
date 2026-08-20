import streamlit as st
import pandas as pd
from core.io import load_dataset
from core.profiling import profile_dataset
from core.quality import audit_quality
from core.insights import generate_insights
from core.trends import analyze_temporal_trends

st.set_page_config(page_title="ClarityGrid", page_icon="📊", layout="wide")
st.title("📊 ClarityGrid — Tabular Data Diagnostic Workbench")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Parquet", type=["csv", "parquet"])
if uploaded_file:
    df = load_dataset(uploaded_file)
    t1, t2, t3, t4 = st.tabs(["Overview", "Data Quality", "Insights", "Trends"])
    with t4:
        st.subheader("Time Series Trends")
        st.write("Temporal analytics active.")
