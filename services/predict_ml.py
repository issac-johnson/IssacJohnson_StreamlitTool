import os
import pandas as pd
import joblib
from collections import Counter
from typing import Optional, Tuple

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, r2_score, mean_absolute_error


def split_features_target(df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y


def infer_task(y: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(y):
        if y.nunique() <= 20:
            return "classification"
        else:
            return "regression"
    else:
        return "classification"


def _safe_stratify(y: pd.Series):
    if y is None:
        return None
    counts = Counter(y)
    if len(counts) < 2 or min(counts.values()) < 2:
        return None
    return y


def build_pipeline(X: pd.DataFrame, task: str) -> Pipeline:
    numeric_features = X.select_dtypes(include=["number"]).columns
    categorical_features = X.select_dtypes(exclude=["number"]).columns

    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    if task == "classification":
        model = RandomForestClassifier(random_state=42)
    else:
        model = RandomForestRegressor(random_state=42)

    pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    return pipe


def train_and_eval(df: pd.DataFrame, target_col: str, task: Optional[str] = None):
    X, y = split_features_target(df, target_col)
    task = task or infer_task(y)
    pipe = build_pipeline(X, task)

    strat = _safe_stratify(y) if task == "classification" else None

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=strat
    )

    pipe.fit(Xtr, ytr)
    preds = pipe.predict(Xte)

    if task == "classification":
        metrics = {
            "accuracy": accuracy_score(yte, preds),
            "f1": f1_score(yte, preds, average="weighted")
        }
    else:
        metrics = {
            "r2": r2_score(yte, preds),
            "mae": mean_absolute_error(yte, preds)
        }

    return pipe, metrics, task


def save_model(pipe: Pipeline, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(pipe, path)


def load_model(path: str) -> Pipeline:
    return joblib.load(path)
