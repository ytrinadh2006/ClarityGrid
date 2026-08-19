import pytest
import pandas as pd
import numpy as np
from core.trends import analyze_temporal_trends

def test_analyze_temporal_trends():
    dates = pd.date_range("2026-01-01", periods=10, freq="D")
    df = pd.DataFrame({"dt": dates, "val": np.arange(10)})
    res = analyze_temporal_trends(df, date_col="dt", value_col="val")
    assert "rolling_7d" in res.columns
    assert len(res) == 10
