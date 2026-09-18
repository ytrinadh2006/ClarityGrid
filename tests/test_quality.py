import pandas as pd
from core.quality import quality_report


def test_quality_report_counts_missing_and_duplicates():
    df = pd.DataFrame({"a": [1, 1, None], "b": ["x", "x", "y"]})
    report = quality_report(df)
    assert report["rows"] == 3
    assert report["columns"] == 2
    assert report["missing_cells"] == 1
    assert report["duplicate_rows"] == 1
