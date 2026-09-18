from __future__ import annotations

import pandas as pd


def generate_quality_insights(report: dict) -> list[str]:
    findings = []
    if report["missing_cells"]:
        findings.append(
            f"There are {report['missing_cells']:,} missing cells ({report['missing_percent']:.1f}% of the table)."
        )
    else:
        findings.append("No missing cells were found in the uploaded table.")

    if report["duplicate_rows"]:
        findings.append(f"There are {report['duplicate_rows']:,} duplicate rows that may need review.")
    else:
        findings.append("No exact duplicate rows were found.")

    if report["constant_columns"]:
        findings.append("Constant columns found: " + ", ".join(report["constant_columns"]) + ".")
    return findings


def generate_numeric_insights(df: pd.DataFrame) -> list[str]:
    findings = []
    for col in df.select_dtypes(include="number").columns[:8]:
        s = df[col].dropna()
        if len(s) < 3:
            continue
        mean = s.mean()
        median = s.median()
        if mean > median * 1.15:
            findings.append(f"{col}: the mean is noticeably above the median, suggesting some higher values are pulling the average up.")
        elif median > mean * 1.15:
            findings.append(f"{col}: the median is noticeably above the mean, so a few lower values may be pulling the average down.")
    return findings


def generate_category_insights(df: pd.DataFrame) -> list[str]:
    findings = []
    for col in df.select_dtypes(include=["object", "category", "bool"]).columns[:8]:
        counts = df[col].value_counts(dropna=True)
        if len(counts) >= 2:
            top = counts.index[0]
            share = counts.iloc[0] / counts.sum() * 100
            if share >= 60:
                findings.append(f"{col}: '{top}' is the dominant category at about {share:.0f}% of non-missing records.")
    return findings


def generate_all_insights(df: pd.DataFrame, report: dict) -> list[str]:
    return generate_quality_insights(report) + generate_numeric_insights(df) + generate_category_insights(df)
