import pandas as pd
from core.quality import quality_report
from core.insights import generate_all_insights


def test_insights_are_generated_for_basic_table():
    df = pd.DataFrame({"sales": [10, 10, 10, 100], "region": ["N", "N", "N", "N"]})
    findings = generate_all_insights(df, quality_report(df))
    assert findings
    assert any("sales" in item for item in findings)
