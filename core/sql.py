import sqlite3
import pandas as pd

class SQLExecutor:
    def __init__(self, tables):
        self.conn = sqlite3.connect(":memory:")
        for name, df in tables.items():
            df.to_sql(name, self.conn, index=False)
            
    def execute(self, query: str):
        return pd.read_sql_query(query, self.conn)
