# 🛰️ Automated NASA Near-Earth Object (NEO) Threat Classifier

An end-to-end machine learning pipeline ingesting live orbital and physical telemetry from **NASA's NeoWs API** to classify Near-Earth Objects into four risk tiers. Automated via **GitHub Actions** for daily live flyby scoring and weekly model retraining.

### 📊 Latest Model Snapshot
* **Last Daily Scan (UTC):** `2026-11-24`
* **Training Catalog Size:** `1000` unique NEOs
* **Validation Macro F1:** `0.9725`
* **High-Threat (PHA/Sentry) Recall:** `1.0`

### ☄️ Today's Close-Approach Predictions (2026-11-24)
| Asteroid | Est. Diameter (km) | Min Miss Distance (km) | Predicted Threat Tier | Actual NASA PHA |
| :--- | :---: | :---: | :--- | :---: |
| 481442 (2006 WO3) | 0.208 | 20,152,442 | **High (Flagged PHA)** | False |
| (2005 UX5) | 0.249 | 36,576,877 | **High (Flagged PHA)** | False |
| (2015 NG3) | 0.197 | 51,265,373 | **High (Flagged PHA)** | False |
| (2006 KK89) | 0.126 | 16,685,425 | **Low (Routine)** | False |
| (2017 RK15) | 0.031 | 44,352,994 | **Low (Routine)** | False |
| (2018 YG) | 0.059 | 58,286,693 | **Low (Routine)** | False |
| (2010 GK65) | 0.054 | 70,436,856 | **Low (Routine)** | False |
