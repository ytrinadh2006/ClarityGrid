import pandas as pd
from typing import BinaryIO, Union

def load_dataset(file_or_path: Union[str, BinaryIO]) -> pd.DataFrame:
    if isinstance(file_or_path, str):
        if file_or_path.endswith('.csv'):
            return pd.read_csv(file_or_path)
    return pd.read_csv(file_or_path)
