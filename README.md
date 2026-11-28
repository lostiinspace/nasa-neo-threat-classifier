# 🛰️ Automated NASA Near-Earth Object (NEO) Threat Classifier

An end-to-end machine learning pipeline ingesting live orbital and physical telemetry from **NASA's NeoWs API** to classify Near-Earth Objects into four risk tiers. Automated via **GitHub Actions** for daily live flyby scoring and weekly model retraining.

### 📊 Latest Model Snapshot
* **Last Daily Scan (UTC):** `2026-11-28`
* **Training Catalog Size:** `1000` unique NEOs
* **Validation Macro F1:** `0.9725`
* **High-Threat (PHA/Sentry) Recall:** `1.0`

### ☄️ Today's Close-Approach Predictions (2026-11-28)
| Asteroid | Est. Diameter (km) | Min Miss Distance (km) | Predicted Threat Tier | Actual NASA PHA |
| :--- | :---: | :---: | :--- | :---: |
| 217628 Lugh (1990 HA) | 1.984 | 10,586,568 | **High (Flagged PHA)** | True |
| (2011 UE305) | 0.244 | 22,973,338 | **High (Flagged PHA)** | True |
| (2005 JQ81) | 0.409 | 33,956,055 | **High (Flagged PHA)** | False |
| (2015 FU284) | 0.009 | 47,173,474 | **Low (Routine)** | False |
| (2016 CN248) | 0.015 | 66,246,803 | **Low (Routine)** | False |
| (2008 WK60) | 0.142 | 72,250,447 | **Low (Routine)** | False |
