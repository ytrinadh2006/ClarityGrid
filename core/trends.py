from __future__ import annotations

import numpy as np
import pandas as pd


def detect_date_column(df: pd.DataFrame) -> str | None:
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col
        if df[col].dtype == "object":
            converted = pd.to_datetime(df[col], errors="coerce")
            if converted.notna().mean() >= 0.8:
                return col
    return None


def prepare_time_series(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    out = pd.DataFrame({"date": pd.to_datetime(df[date_col], errors="coerce"), "value": pd.to_numeric(df[value_col], errors="coerce")})
    out = out.dropna().sort_values("date")
    return out.groupby("date", as_index=False)["value"].sum()


def rolling_trend(series: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    out = series.copy()
    out["rolling_mean"] = out["value"].rolling(window, min_periods=1).mean()
    return out


def iqr_anomalies(df: pd.DataFrame, column: str) -> pd.DataFrame:
    values = pd.to_numeric(df[column], errors="coerce")
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    if pd.isna(iqr) or iqr == 0:
        return pd.DataFrame(columns=["row", column, "reason"])
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mask = (values < low) | (values > high)
    result = pd.DataFrame({"row": df.index[mask], column: values[mask]})
    result["reason"] = np.where(values[mask] < low, "below IQR range", "above IQR range")
    return result.reset_index(drop=True)


def simple_forecast(series: pd.DataFrame, periods: int = 5) -> pd.DataFrame:
    if len(series) < 3:
        raise ValueError("At least three time points are needed for the baseline forecast.")
    x = np.arange(len(series)).reshape(-1, 1)
    y = series["value"].to_numpy()
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(x, y)
    future_x = np.arange(len(series), len(series) + periods).reshape(-1, 1)
    start = series["date"].max()
    freq = series["date"].sort_values().diff().median()
    if pd.isna(freq) or freq <= pd.Timedelta(0):
        freq = pd.Timedelta(days=1)
    dates = [start + freq * (i + 1) for i in range(periods)]
    return pd.DataFrame({"date": dates, "forecast": model.predict(future_x)})
