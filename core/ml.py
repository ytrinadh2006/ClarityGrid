from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def infer_task(target: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(target) and target.nunique(dropna=True) > 10:
        return "regression"
    return "classification"


def run_experiment(df: pd.DataFrame, target: str, task: str | None = None) -> dict:
    work = df.dropna(subset=[target]).copy()
    y = work.pop(target)
    task = task or infer_task(y)
    if len(work) < 20:
        raise ValueError("At least 20 usable rows are recommended for the ML experiment.")

    numeric = work.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in work.columns if c not in numeric]
    transformers = []
    if numeric:
        transformers.append(("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric))
    if categorical:
        transformers.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical))
    preprocessor = ColumnTransformer(transformers)

    if task == "classification":
        if y.nunique() < 2:
            raise ValueError("The target needs at least two classes.")
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42),
        }
    else:
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=150, random_state=42),
        }

    stratify = y if task == "classification" and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(work, y, test_size=0.2, random_state=42, stratify=stratify)
    results = []
    fitted = {}
    for name, estimator in models.items():
        pipe = Pipeline([("prep", preprocessor), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        if task == "classification":
            metric = accuracy_score(y_test, pred)
            row = {"model": name, "primary_metric": "accuracy", "score": round(float(metric), 4)}
            if y_test.nunique() == 2 and hasattr(pipe, "predict_proba"):
                try:
                    row["roc_auc"] = round(float(roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])), 4)
                except ValueError:
                    pass
            results.append(row)
        else:
            mae = mean_absolute_error(y_test, pred)
            rmse = mean_squared_error(y_test, pred) ** 0.5
            r2 = r2_score(y_test, pred)
            results.append({"model": name, "MAE": round(float(mae), 4), "RMSE": round(float(rmse), 4), "R2": round(float(r2), 4)})
        fitted[name] = pipe

    best_name = max(results, key=lambda x: x.get("score", x.get("R2", float("-inf"))))["model"]

    # A small cross-validation check gives a more stable view than one split alone.
    cv_results = []
    cv_splits = 5 if len(work) >= 50 else 3
    for name, estimator in models.items():
        pipe = Pipeline([("prep", preprocessor), ("model", estimator)])
        try:
            if task == "classification":
                min_class = int(y.value_counts().min())
                folds = min(cv_splits, min_class)
                if folds >= 2:
                    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
                    scores = cross_val_score(pipe, work, y, cv=cv, scoring="accuracy")
                    cv_results.append({"model": name, "metric": "cv_accuracy", "mean": round(float(scores.mean()), 4), "std": round(float(scores.std()), 4)})
            else:
                cv = KFold(n_splits=cv_splits, shuffle=True, random_state=42)
                scores = cross_val_score(pipe, work, y, cv=cv, scoring="r2")
                cv_results.append({"model": name, "metric": "cv_r2", "mean": round(float(scores.mean()), 4), "std": round(float(scores.std()), 4)})
        except ValueError:
            pass
    best = fitted[best_name]
    feature_importance = []
    model = best.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        names = best.named_steps["prep"].get_feature_names_out()
        feature_importance = sorted(
            [{"feature": n.replace("num__", "").replace("cat__", ""), "importance": float(v)} for n, v in zip(names, model.feature_importances_)],
            key=lambda x: x["importance"], reverse=True,
        )[:10]

    evaluation = {}
    if task == "classification":
        evaluation["confusion_matrix"] = confusion_matrix(y_test, best.predict(X_test)).tolist()
    else:
        evaluation["test_predictions"] = {"actual": y_test.tolist(), "predicted": best.predict(X_test).tolist()}

    return {"task": task, "target": target, "results": results, "cv_results": cv_results, "best_model": best_name, "feature_importance": feature_importance, "evaluation": evaluation}
