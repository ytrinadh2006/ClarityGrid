from __future__ import annotations

import pandas as pd


def quality_report(df: pd.DataFrame) -> dict:
    """Return simple, explainable data-quality checks."""
    rows, cols = df.shape
    cells = max(rows * cols, 1)
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    constant_columns = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]

    score = 100.0
    score -= min(40.0, missing / cells * 100)
    score -= min(30.0, duplicates / max(rows, 1) * 100)
    score -= min(20.0, len(constant_columns) / max(cols, 1) * 100)
    score = round(max(0.0, score), 1)

    return {
        "rows": rows,
        "columns": cols,
        "missing_cells": missing,
        "missing_percent": round(missing / cells * 100, 2),
        "duplicate_rows": duplicates,
        "constant_columns": constant_columns,
        "score": score,
    }
