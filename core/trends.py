import pandas as pd
import numpy as np

def detect_iqr_outliers(series: pd.Series, factor: float = 1.5):
    q25, q75 = np.percentile(series.dropna(), [25, 75])
    iqr = q75 - q25
    lower = q25 - factor * iqr
    upper = q75 + factor * iqr
    return (series < lower) | (series > upper)
