from __future__ import annotations

from io import BytesIO
import pandas as pd


def read_uploaded_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Read a CSV or Excel upload into a DataFrame."""
    lower = filename.lower()
    buffer = BytesIO(file_bytes)
    if lower.endswith(".csv"):
        return pd.read_csv(buffer)
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(buffer)
    raise ValueError("Please upload a CSV or Excel file.")
