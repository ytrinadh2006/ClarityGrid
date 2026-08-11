import pandas as pd
from dataclasses import dataclass
from typing import Dict

@dataclass
class QualityReport:
    missing_by_column: Dict[str, float]
    total_missing_cells: int
    health_score: int

def audit_quality(df: pd.DataFrame) -> QualityReport:
    missing = df.isna().sum().to_dict()
    total = sum(missing.values())
    score = max(0, 100 - int((total / (df.size or 1)) * 100))
    return QualityReport(missing, total, score)
