from __future__ import annotations

import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from core.io import read_uploaded_file
from core.quality import quality_report
from core.profiling import numeric_summary, profile_columns
from core.insights import generate_all_insights
from core.ml import run_experiment
from core.storage import recent_sessions, save_session
from core.sql import run_read_only_query, sample_queries
from core.trends import detect_date_column, iqr_anomalies, prepare_time_series, rolling_trend, simple_forecast

st.set_page_config(page_title="ClarityGrid", page_icon="▦", layout="wide")
st.title("ClarityGrid")
st.caption("A practical workspace for turning a raw table into a clearer analysis.")

uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
if uploaded is None:
    st.info("Upload a dataset to start. A small sample is available in data/sample/orders.csv.")
    st.markdown("### What happens next")
    st.write("ClarityGrid checks the data first, then gives you a profile, visual exploration, findings, and an optional ML experiment.")
    st.stop()

try:
    df = read_uploaded_file(uploaded.getvalue(), uploaded.name)
except Exception as exc:
    st.error(str(exc))
    st.stop()

report = quality_report(df)
profile = profile_columns(df)
insights = generate_all_insights(df, report)

with st.sidebar:
    st.header("Dataset")
    st.write(uploaded.name)
    st.metric("Rows", f"{len(df):,}")
    st.metric("Columns", f"{len(df.columns):,}")
    st.metric("Quality", f"{report['score']}/100")
    page = st.radio("Go to", ["Overview", "Explore", "Insights", "Trends & anomalies", "SQL workspace", "ML lab", "History"])

if page == "Overview":
    st.subheader("Quick overview")
    a, b, c, d = st.columns(4)
    a.metric("Rows", f"{report['rows']:,}")
    b.metric("Columns", f"{report['columns']:,}")
    c.metric("Missing cells", f"{report['missing_cells']:,}")
    d.metric("Duplicate rows", f"{report['duplicate_rows']:,}")
    st.markdown("### Column profile")
    st.dataframe(profile, width="stretch", hide_index=True)
    st.markdown("### Numeric summary")
    summary = numeric_summary(df)
    if summary.empty:
        st.info("No numeric columns were found.")
    else:
        st.dataframe(summary, width="stretch", hide_index=True)
    st.markdown("### Data-quality notes")
    for item in insights[:5]:
        st.write("•", item)

elif page == "Explore":
    st.subheader("Explore the data")
    st.dataframe(df.head(100), width="stretch")
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    if numeric:
        col = st.selectbox("Numeric column", numeric)
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        st.pyplot(fig)
        plt.close(fig)
    if categorical:
        col = st.selectbox("Categorical column", categorical, key="cat")
        counts = df[col].value_counts().head(15)
        st.bar_chart(counts)
    if len(numeric) >= 2:
        st.markdown("### Correlation")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(df[numeric].corr(), annot=True, fmt=".2f", ax=ax)
        st.pyplot(fig)
        plt.close(fig)

elif page == "Insights":
    st.subheader("What stands out")
    if not insights:
        st.info("No simple findings were triggered for this dataset.")
    for i, item in enumerate(insights, 1):
        st.write(f"**{i}.** {item}")
    payload = {"quality": report, "insights": insights}
    st.download_button("Download findings JSON", json.dumps(payload, indent=2, default=str), file_name="claritygrid_findings.json", mime="application/json")
    if st.button("Save this analysis"):
        save_session(uploaded.name, payload, datetime.now().isoformat(timespec="seconds"))
        st.success("Analysis saved locally.")

elif page == "Trends & anomalies":
    st.subheader("Trends and anomalies")
    date_col = detect_date_column(df)
    numeric = df.select_dtypes(include="number").columns.tolist()
    if not date_col:
        st.info("I could not confidently identify a date column. Add a date-like column to use the trend section.")
    elif not numeric:
        st.info("A numeric column is needed for trend analysis.")
    else:
        st.write(f"Detected date column: **{date_col}**")
        value_col = st.selectbox("Value column", numeric)
        series = prepare_time_series(df, date_col, value_col)
        trend = rolling_trend(series)
        st.line_chart(trend.set_index("date")[['value', 'rolling_mean']])
        st.markdown("### Unusual values")
        anomaly_col = st.selectbox("Check for IQR anomalies", numeric, key="anomaly")
        anomalies = iqr_anomalies(df, anomaly_col)
        if anomalies.empty:
            st.success("No IQR-based anomalies were found.")
        else:
            st.dataframe(anomalies, width="stretch", hide_index=True)
        st.markdown("### Baseline forecast")
        periods = st.slider("Future periods", 1, 12, 5)
        if st.button("Build forecast"):
            forecast = simple_forecast(series, periods)
            st.dataframe(forecast, width="stretch", hide_index=True)

elif page == "SQL workspace":
    st.subheader("SQL workspace")
    st.caption("The query runs against an in-memory copy of the uploaded table. Only read-only SELECT/WITH queries are accepted.")
    examples = sample_queries(df.columns.tolist())
    if examples:
        example = st.selectbox("Example query", ["Choose an example"] + examples)
    else:
        example = "Choose an example"
    default_query = examples[0] if examples and example == "Choose an example" else (example if example != "Choose an example" else "SELECT * FROM dataset LIMIT 20")
    query = st.text_area("SQL query", value=default_query, height=140)
    if st.button("Run query"):
        try:
            result_df = run_read_only_query(df, query)
            st.success(f"Returned {len(result_df):,} rows.")
            st.dataframe(result_df, width="stretch", hide_index=True)
        except Exception as exc:
            st.error(str(exc))

elif page == "ML lab":
    st.subheader("Small ML experiment")
    st.caption("This is an experiment area, not an AutoML system.")
    target = st.selectbox("Target column", list(df.columns))
    task = st.selectbox("Task", ["Automatic", "classification", "regression"])
    if st.button("Run experiment"):
        try:
            result = run_experiment(df, target, None if task == "Automatic" else task)
            st.write(f"Detected task: **{result['task']}**")
            st.write(f"Best model: **{result['best_model']}**")
            st.markdown("### Test-set comparison")
            st.dataframe(pd.DataFrame(result['results']), width="stretch", hide_index=True)
            if result.get("cv_results"):
                st.markdown("### Cross-validation check")
                st.dataframe(pd.DataFrame(result["cv_results"]), width="stretch", hide_index=True)
            if result["task"] == "classification" and result.get("evaluation", {}).get("confusion_matrix"):
                st.markdown("### Confusion matrix")
                st.dataframe(pd.DataFrame(result["evaluation"]["confusion_matrix"]), width="stretch", hide_index=True)
            if result['feature_importance']:
                st.markdown("### Most important features")
                st.dataframe(pd.DataFrame(result['feature_importance']), width="stretch", hide_index=True)
        except Exception as exc:
            st.error(str(exc))

else:
    st.subheader("Saved analyses")
    sessions = recent_sessions()
    if not sessions:
        st.info("No saved analyses yet.")
    else:
        for session in sessions:
            with st.expander(f"{session['filename']} — {session['created_at']}"):
                st.json(session['payload'])
