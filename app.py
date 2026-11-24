import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="NASA NEO Threat Classifier", layout="wide")
st.title("🛰️ Live Near-Earth Object (NEO) Threat Classifier")
st.caption("Automated ML pipeline ingesting daily telemetry from NASA's NeoWs API.")

if os.path.exists("data/latest_predictions.csv") and os.path.exists("metrics_history.json"):
    preds = pd.read_csv("data/latest_predictions.csv")
    with open("metrics_history.json", "r", encoding="utf-8") as f:
        history = pd.DataFrame(json.load(f))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Today's Tracked Flybys", len(preds))
    col2.metric("Flagged High/Critical (Tier 2–3)", int((preds["predicted_threat_level"] >= 2).sum()))
    col3.metric("Catalog Size", f"{history['total_neos'].iloc[-1]:,}")
    col4.metric("Latest Model Macro F1", f"{history['macro_f1'].iloc[-1]:.3f}")

    st.subheader("Today's Close Approaches (Live Model Inference)")
    st.dataframe(preds, use_container_width=True)

    st.subheader("Model Evolution Over Weekly Retraining Runs")
    st.line_chart(history.set_index("run_date")[["macro_f1", "pha_recall"]])
else:
    st.info("Waiting for first GitHub Actions pipeline run to generate predictions.")