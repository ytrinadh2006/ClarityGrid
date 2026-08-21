from __future__ import annotations

import sqlite3
import re

import pandas as pd


def _quote_identifier(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def dataframe_to_sql(df: pd.DataFrame, table_name: str = "dataset") -> str:
    with sqlite3.connect(":memory:") as con:
        df.to_sql(table_name, con, index=False, if_exists="replace")
        return table_name


def run_read_only_query(df: pd.DataFrame, query: str, table_name: str = "dataset") -> pd.DataFrame:
    """Run a SELECT/WITH query against an in-memory copy of the uploaded data."""
    cleaned = query.strip().rstrip(";").strip()
    if not cleaned:
        raise ValueError("Enter a SQL query first.")
    if not re.match(r"^(select|with)\b", cleaned, flags=re.IGNORECASE):
        raise ValueError("Only SELECT and WITH queries are allowed in the SQL workspace.")

    forbidden = re.search(r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|replace|vacuum)\b", cleaned, flags=re.IGNORECASE)
    if forbidden:
        raise ValueError(f"'{forbidden.group(1).upper()}' statements are not allowed here.")

    with sqlite3.connect(":memory:") as con:
        df.to_sql(table_name, con, index=False, if_exists="replace")
        return pd.read_sql_query(cleaned, con)


def sample_queries(columns: list[str]) -> list[str]:
    if not columns:
        return []
    first = _quote_identifier(columns[0])
    return [
        'SELECT * FROM dataset LIMIT 20',
        f'SELECT {first}, COUNT(*) AS row_count FROM dataset GROUP BY {first} ORDER BY row_count DESC LIMIT 10',
    ]
