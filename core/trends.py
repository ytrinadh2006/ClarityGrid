import pandas as pd

def detect_date_columns(df: pd.DataFrame):
    date_cols = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_cols.append(col)
        elif "date" in col.lower() or "time" in col.lower():
            date_cols.append(col)
    return date_cols
