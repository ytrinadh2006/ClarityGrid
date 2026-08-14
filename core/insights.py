import pandas as pd
from dataclasses import dataclass
from typing import List

@dataclass
class Insight:
    title: str
    description: str
    severity: str

def generate_insights(df: pd.DataFrame) -> List[Insight]:
    insights = []
    for col in df.columns:
        if df[col].nunique() == 1:
            insights.append(Insight("Zero Variance", f"Column '{col}' has only 1 unique value.", "WARNING"))
    return insights
