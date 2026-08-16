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
    tab_overview, tab_quality, tab_insights = st.tabs(["Overview", "Data Quality", "Automated Insights"])
    with tab_overview:
        col1, col2 = st.columns(2)
        col1.metric("Rows", f"{len(df):,}")
        col2.metric("Columns", len(df.columns))
        st.dataframe(df.head(15))
    with tab_quality:
        rep = audit_quality(df)
        st.metric("Health Score", f"{rep.health_score}/100")
        st.bar_chart(pd.Series(rep.missing_by_column))
    with tab_insights:
        for ins in generate_insights(df):
            st.warning(f"**{ins.title}**: {ins.description}")
