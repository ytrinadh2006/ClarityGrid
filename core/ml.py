import pandas as pd

def detect_target_task(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series) and series.nunique() > 10:
        return "regression"
    return "classification"
