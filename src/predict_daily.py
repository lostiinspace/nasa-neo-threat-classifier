import json
import os
from datetime import datetime, timezone

import joblib
import pandas as pd
import requests

try:
    from src.features import (
        THREAT_LABELS,
        engineer_features_and_labels,
        parse_neo_record,
    )
    from src.train import METRICS_PATH, MODEL_PATH, run_training
except ImportError:
    from features import (
        THREAT_LABELS,
        engineer_features_and_labels,
        parse_neo_record,
    )
    from train import METRICS_PATH, MODEL_PATH, run_training

FEED_URL = "https://api.nasa.gov/neo/rest/v1/feed"
PREDICTIONS_PATH = "data/latest_predictions.csv"


def update_readme(today_str: str, preds_df: pd.DataFrame) -> None:
    latest_metrics = {"total_neos": "N/A", "macro_f1": "N/A", "pha_recall": "N/A"}
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
            if history:
                latest_metrics = history[-1]

    table_lines = [
        "| Asteroid | Est. Diameter (km) | Min Miss Distance (km) | Predicted Threat Tier | Actual NASA PHA |",
        "| :--- | :---: | :---: | :--- | :---: |",
    ]
    for _, row in preds_df.head(10).iterrows():
        table_lines.append(
            f"| {row['name']} | {row['diameter_mean_km']:.3f} | "
            f"{row['min_miss_distance_km']:,.0f} | **{row['threat_label']}** | {row['is_pha']} |"
        )

    readme_content = f"""# 🛰️ Automated NASA Near-Earth Object (NEO) Threat Classifier

An end-to-end machine learning pipeline ingesting live orbital and physical telemetry from **NASA's NeoWs API** to classify Near-Earth Objects into four risk tiers. Automated via **GitHub Actions** for daily live flyby scoring and weekly model retraining.

### 📊 Latest Model Snapshot
* **Last Daily Scan (UTC):** `{today_str}`
* **Training Catalog Size:** `{latest_metrics['total_neos']}` unique NEOs
* **Validation Macro F1:** `{latest_metrics['macro_f1']}`
* **High-Threat (PHA/Sentry) Recall:** `{latest_metrics['pha_recall']}`

### ☄️ Today's Close-Approach Predictions ({today_str})
{chr(10).join(table_lines)}
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)


def run_daily_inference() -> None:
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        raise RuntimeError("NASA_API_KEY environment variable is missing.")

    if not os.path.exists(MODEL_PATH):
        print("No trained model found. Running initial training pipeline first...")
        run_training()

    clf = joblib.load(MODEL_PATH)
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    resp = requests.get(
        FEED_URL,
        params={"start_date": today_str, "end_date": today_str, "api_key": api_key},
        timeout=15,
    )
    resp.raise_for_status()
    neos_today = resp.json().get("near_earth_objects", {}).get(today_str, [])

    rows = [parse_neo_record(neo) for neo in neos_today]
    df = engineer_features_and_labels(pd.DataFrame(rows))

    preds = clf.predict(df)
    probs = clf.predict_proba(df)
    classes = list(clf.classes_)

    df["predicted_threat_level"] = preds
    df["threat_label"] = [THREAT_LABELS[int(c)] for c in preds]
    df["high_threat_prob"] = [
        round(sum(p[i] for i, cls in enumerate(classes) if cls >= 2), 4)
        for p in probs
    ]

    output_cols = [
        "neo_id",
        "name",
        "diameter_mean_km",
        "min_miss_distance_km",
        "mean_rel_velocity_kps",
        "predicted_threat_level",
        "threat_label",
        "high_threat_prob",
        "is_pha",
        "is_sentry",
    ]
    out_df = df[output_cols].sort_values(
        by=["predicted_threat_level", "min_miss_distance_km"], ascending=[False, True]
    )

    os.makedirs("data", exist_ok=True)
    out_df.to_csv(PREDICTIONS_PATH, index=False)
    update_readme(today_str, out_df)
    print(f"Scored {len(out_df)} flybys for {today_str} and updated README.md.")


if __name__ == "__main__":
    run_daily_inference()