import pandas as pd
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DatasetProfile:
    row_count: int
    col_count: int
    memory_bytes: int
    column_types: Dict[str, str]

def profile_dataset(df: pd.DataFrame) -> DatasetProfile:
    return DatasetProfile(
        row_count=len(df),
        col_count=len(df.columns),
        memory_bytes=df.memory_usage(deep=True).sum(),
        column_types={col: str(dtype) for col, dtype in df.dtypes.items()}
    )
