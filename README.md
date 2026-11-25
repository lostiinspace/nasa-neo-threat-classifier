# 🛰️ Automated NASA Near-Earth Object (NEO) Threat Classifier

An end-to-end machine learning pipeline ingesting live orbital and physical telemetry from **NASA's NeoWs API** to classify Near-Earth Objects into four risk tiers. Automated via **GitHub Actions** for daily live flyby scoring and weekly model retraining.

### 📊 Latest Model Snapshot
* **Last Daily Scan (UTC):** `2026-11-25`
* **Training Catalog Size:** `1000` unique NEOs
* **Validation Macro F1:** `0.9725`
* **High-Threat (PHA/Sentry) Recall:** `1.0`

### ☄️ Today's Close-Approach Predictions (2026-11-25)
| Asteroid | Est. Diameter (km) | Min Miss Distance (km) | Predicted Threat Tier | Actual NASA PHA |
| :--- | :---: | :---: | :--- | :---: |
| (2016 WD10) | 0.216 | 58,068,022 | **High (Flagged PHA)** | False |
| 455659 (2005 BO1) | 0.206 | 72,735,858 | **High (Flagged PHA)** | False |
| (2018 VL8) | 0.118 | 10,826,838 | **Low (Routine)** | False |
| (2009 WS25) | 0.041 | 23,469,700 | **Low (Routine)** | False |
| (2014 US7) | 0.021 | 24,137,401 | **Low (Routine)** | False |
| (2003 UY12) | 0.095 | 30,285,832 | **Low (Routine)** | False |
| (2015 BG4) | 0.023 | 53,055,212 | **Low (Routine)** | False |
| (2014 MW26) | 0.116 | 58,891,661 | **Low (Routine)** | False |
| (2019 AS) | 0.021 | 63,898,382 | **Low (Routine)** | False |
