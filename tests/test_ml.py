import pytest
import pandas as pd
import numpy as np
from core.ml import train_baseline_model

def test_baseline_regression():
    df = pd.DataFrame({"x": np.arange(30), "y": np.arange(30) * 2})
    res = train_baseline_model(df, target_col="y")
    assert res.task_type == "regression"
    assert res.metrics["r2"] > 0.95
