import pytest
import pandas as pd
from core.sql import SQLExecutor

def test_sql_read():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    executor = SQLExecutor({"tbl": df})
    res = executor.execute("SELECT COUNT(*) as cnt FROM tbl")
    assert res.iloc[0]["cnt"] == 2

def test_sql_block_mutation():
    df = pd.DataFrame({"a": [1]})
    executor = SQLExecutor({"tbl": df})
    with pytest.raises(ValueError):
        executor.execute("DROP TABLE tbl")
