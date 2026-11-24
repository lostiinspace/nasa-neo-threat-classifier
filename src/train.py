import json
import os
import random
from datetime import datetime, timezone
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd
import requests
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from src.features import (
        CATEGORICAL_FEATURES,
        NUMERIC_FEATURES,
        engineer_features_and_labels,
        parse_neo_record,
    )
except ImportError:
    from features import (
        CATEGORICAL_FEATURES,
        NUMERIC_FEATURES,
        engineer_features_and_labels,
        parse_neo_record,
    )

BROWSE_URL = "https://api.nasa.gov/neo/rest/v1/neo/browse"
CATALOG_PATH = "data/neo_catalog.parquet"
MODEL_PATH = "models/neo_threat_model.joblib"
METRICS_PATH = "metrics_history.json"


def fetch_diverse_batch(api_key: str, num_pages: int = 50, page_size: int = 20) -> pd.DataFrame:
    probe = requests.get(
        BROWSE_URL, params={"page": 0, "size": page_size, "api_key": api_key}, timeout=15
    )
    probe.raise_for_status()
    total_pages = probe.json()["page"]["total_pages"]

    sampled_pages = random.sample(range(total_pages), k=min(num_pages, total_pages))
    records: List[Dict[str, Any]] = []

    for idx, page_num in enumerate(sampled_pages, start=1):
        resp = requests.get(
            BROWSE_URL,
            params={"page": page_num, "size": page_size, "api_key": api_key},
            timeout=15,
        )
        resp.raise_for_status()
        for neo in resp.json().get("near_earth_objects", []):
            records.append(parse_neo_record(neo))

        if idx % 10 == 0:
            print(f"Fetched {idx}/{num_pages} catalog pages ({len(records)} records)")

    return pd.DataFrame(records)


def run_training() -> None:
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        raise RuntimeError("NASA_API_KEY environment variable is missing.")

    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    new_df = fetch_diverse_batch(api_key=api_key, num_pages=50, page_size=20)

    if os.path.exists(CATALOG_PATH):
        existing_df = pd.read_parquet(CATALOG_PATH)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=["neo_id"], keep="last")
    else:
        combined_df = new_df.drop_duplicates(subset=["neo_id"], keep="last")

    combined_df.to_parquet(CATALOG_PATH, index=False)
    print(f"Rolling catalog size: {len(combined_df)} unique NEOs")

    dataset = engineer_features_and_labels(combined_df)
    X = dataset[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = dataset["threat_level"]

    stratify_target = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=stratify_target
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]),
                NUMERIC_FEATURES,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="constant", fill_value="UNKNOWN")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                ]),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    clf = Pipeline([
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=14,
                class_weight="balanced_subsample",
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ])

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    joblib.dump(clf, MODEL_PATH)

    macro_f1 = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    y_test_high = (y_test >= 2).astype(int)
    y_pred_high = (y_pred >= 2).astype(int)
    pha_recall = float(recall_score(y_test_high, y_pred_high, zero_division=0))

    history = []
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)

    history.append({
        "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total_neos": int(len(combined_df)),
        "macro_f1": round(macro_f1, 4),
        "pha_recall": round(pha_recall, 4),
    })

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"Model saved! Macro F1: {macro_f1:.4f} | High-Threat Recall: {pha_recall:.4f}")


if __name__ == "__main__":
    run_training()