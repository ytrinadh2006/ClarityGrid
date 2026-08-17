import pandas as pd
import numpy as np

def analyze_temporal_trends(df: pd.DataFrame, date_col: str, value_col: str, freq: str = "D"):
    temp_df = df[[date_col, value_col]].dropna().copy()
    temp_df[date_col] = pd.to_datetime(temp_df[date_col])
    temp_df = temp_df.sort_values(by=date_col)
    
    aggregated = temp_df.groupby(pd.Grouper(key=date_col, freq=freq))[value_col].agg(['sum', 'mean', 'count']).reset_index()
    aggregated['rolling_7d'] = aggregated['mean'].rolling(window=7, min_periods=1).mean()
    aggregated['rolling_30d'] = aggregated['mean'].rolling(window=30, min_periods=1).mean()
    return aggregated
