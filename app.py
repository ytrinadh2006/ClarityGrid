import streamlit as st
import pandas as pd
from core.io import load_dataset
from core.ml import train_baseline_model

st.set_page_config(page_title="ClarityGrid", page_icon="📊", layout="wide")
st.title("📊 ClarityGrid — Tabular Data Diagnostic Workbench")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Parquet", type=["csv", "parquet"])
if uploaded_file:
    df = load_dataset(uploaded_file)
    target = st.sidebar.selectbox("Target Column", df.columns)
    if st.sidebar.button("Train Baseline"):
        res = train_baseline_model(df, target_col=target)
        st.write("Model Metrics:", res.metrics)
