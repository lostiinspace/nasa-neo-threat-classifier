# 🛰️ Automated NASA Near-Earth Object (NEO) Threat Classifier

An end-to-end machine learning pipeline ingesting live orbital and physical telemetry from **NASA's NeoWs API** to classify Near-Earth Objects into four risk tiers. Automated via **GitHub Actions** for daily live flyby scoring and weekly model retraining.

### 📊 Latest Model Snapshot
* **Last Daily Scan (UTC):** `2026-11-26`
* **Training Catalog Size:** `1000` unique NEOs
* **Validation Macro F1:** `0.9725`
* **High-Threat (PHA/Sentry) Recall:** `1.0`

### ☄️ Today's Close-Approach Predictions (2026-11-26)
| Asteroid | Est. Diameter (km) | Min Miss Distance (km) | Predicted Threat Tier | Actual NASA PHA |
| :--- | :---: | :---: | :--- | :---: |
| (2014 QR295) | 0.903 | 41,849,568 | **High (Flagged PHA)** | False |
| (2018 XP3) | 0.116 | 24,149,953 | **Low (Routine)** | False |
| 612197 (2000 WP19) | 0.112 | 62,049,457 | **Low (Routine)** | False |
| (2000 WP19) | 0.124 | 62,049,461 | **Low (Routine)** | False |
