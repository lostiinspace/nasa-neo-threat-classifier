# 🛰️ Automated NASA Near-Earth Object (NEO) Threat Classifier

An end-to-end machine learning pipeline ingesting live orbital and physical telemetry from **NASA's NeoWs API** to classify Near-Earth Objects into four risk tiers. Automated via **GitHub Actions** for daily live flyby scoring and weekly model retraining.

### 📊 Latest Model Snapshot
* **Last Daily Scan (UTC):** `2026-11-27`
* **Training Catalog Size:** `1000` unique NEOs
* **Validation Macro F1:** `0.9725`
* **High-Threat (PHA/Sentry) Recall:** `1.0`

### ☄️ Today's Close-Approach Predictions (2026-11-27)
| Asteroid | Est. Diameter (km) | Min Miss Distance (km) | Predicted Threat Tier | Actual NASA PHA |
| :--- | :---: | :---: | :--- | :---: |
| 706765 (2010 TK7) | 0.300 | 40,546,290 | **High (Flagged PHA)** | False |
| (2010 TK7) | 0.300 | 40,546,291 | **High (Flagged PHA)** | False |
| (2018 TX4) | 0.751 | 45,782,233 | **High (Flagged PHA)** | False |
| (2017 WW12) | 0.358 | 63,684,838 | **High (Flagged PHA)** | False |
| (2010 RJ43) | 0.078 | 20,445,653 | **Low (Routine)** | False |
| (2017 KA5) | 0.033 | 45,320,479 | **Low (Routine)** | False |
| (2007 CM26) | 0.041 | 68,759,730 | **Low (Routine)** | False |
