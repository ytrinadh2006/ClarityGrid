import pandas as pd
from core.trends import iqr_anomalies, prepare_time_series


def test_prepare_time_series_groups_by_date():
    df = pd.DataFrame({"date": ["2026-01-01", "2026-01-01", "2026-01-02"], "value": [10, 20, 5]})
    out = prepare_time_series(df, "date", "value")
    assert len(out) == 2
    assert out.loc[0, "value"] == 30


def test_iqr_finds_large_outlier():
    df = pd.DataFrame({"value": [10, 11, 12, 13, 100]})
    out = iqr_anomalies(df, "value")
    assert len(out) == 1
    assert out.loc[0, "value"] == 100
