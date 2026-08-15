import streamlit as st
import pandas as pd
from core.io import load_dataset
from core.profiling import profile_dataset
from core.quality import audit_quality
from core.insights import generate_insights

st.set_page_config(page_title="ClarityGrid", page_icon="📊", layout="wide")
st.title("📊 ClarityGrid — Tabular Data Diagnostic Workbench")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Parquet", type=["csv", "parquet"])
if uploaded_file:
    df = load_dataset(uploaded_file)
    st.subheader("Automated Diagnostics")
    for ins in generate_insights(df):
        if ins.severity == "CRITICAL":
            st.error(f"**{ins.title}**: {ins.description}")
        elif ins.severity == "WARNING":
            st.warning(f"**{ins.title}**: {ins.description}")
        else:
            st.info(f"**{ins.title}**: {ins.description}")
