from typing import Any, Dict, List
import numpy as np
import pandas as pd

AU_IN_KM = 149_597_870.7

THREAT_LABELS = {
    0: "Low (Routine)",
    1: "Moderate (Close Watch)",
    2: "High (Flagged PHA)",
    3: "Critical (Sentry PHA)",
}

NUMERIC_FEATURES = [
    "absolute_magnitude_h",
    "diameter_min_km",
    "diameter_max_km",
    "diameter_mean_km",
    "minimum_orbit_intersection",
    "eccentricity",
    "semi_major_axis",
    "inclination",
    "orbital_period",
    "perihelion_distance",
    "aphelion_distance",
    "jupiter_tisserand_invariant",
    "orbit_uncertainty",
    "approach_count",
    "min_miss_distance_km",
    "mean_rel_velocity_kps",
    "kinetic_energy_proxy",
    "aphelion_perihelion_ratio",
]

CATEGORICAL_FEATURES = ["orbit_class_type"]


def safe_float(value: Any) -> float:
    try:
        return float(value) if value is not None else np.nan
    except (ValueError, TypeError):
        return np.nan


def parse_neo_record(neo: Dict[str, Any]) -> Dict[str, Any]:
    diam_km = neo.get("estimated_diameter", {}).get("kilometers", {})
    orbital = neo.get("orbital_data", {})
    approaches = neo.get("close_approach_data", [])

    miss_distances_km = [
        safe_float(a.get("miss_distance", {}).get("kilometers")) for a in approaches
    ]
    velocities_kps = [
        safe_float(a.get("relative_velocity", {}).get("kilometers_per_second"))
        for a in approaches
    ]

    d_min = safe_float(diam_km.get("estimated_diameter_min"))
    d_max = safe_float(diam_km.get("estimated_diameter_max"))

    return {
        "neo_id": str(neo.get("id")),
        "name": neo.get("name", "Unknown"),
        "absolute_magnitude_h": safe_float(neo.get("absolute_magnitude_h")),
        "diameter_min_km": d_min,
        "diameter_max_km": d_max,
        "diameter_mean_km": np.nanmean([d_min, d_max]),
        "minimum_orbit_intersection": safe_float(orbital.get("minimum_orbit_intersection")),
        "eccentricity": safe_float(orbital.get("eccentricity")),
        "semi_major_axis": safe_float(orbital.get("semi_major_axis")),
        "inclination": safe_float(orbital.get("inclination")),
        "orbital_period": safe_float(orbital.get("orbital_period")),
        "perihelion_distance": safe_float(orbital.get("perihelion_distance")),
        "aphelion_distance": safe_float(orbital.get("aphelion_distance")),
        "jupiter_tisserand_invariant": safe_float(orbital.get("jupiter_tisserand_invariant")),
        "orbit_uncertainty": safe_float(orbital.get("orbit_uncertainty")),
        "orbit_class_type": orbital.get("orbit_class", {}).get("orbit_class_type", "UNKNOWN"),
        "approach_count": len(approaches),
        "min_miss_distance_km": np.nanmin(miss_distances_km) if miss_distances_km else np.nan,
        "mean_rel_velocity_kps": np.nanmean(velocities_kps) if velocities_kps else np.nan,
        "is_pha": bool(neo.get("is_potentially_hazardous_asteroid", False)),
        "is_sentry": bool(neo.get("is_sentry_object", False)),
    }


def engineer_features_and_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["kinetic_energy_proxy"] = (df["diameter_mean_km"] ** 3) * (
        df["mean_rel_velocity_kps"] ** 2
    )
    df["aphelion_perihelion_ratio"] = df["aphelion_distance"] / df[
        "perihelion_distance"
    ].replace(0, np.nan)

    conditions = [
        df["is_pha"] & df["is_sentry"],
        df["is_pha"] & (~df["is_sentry"]),
        (~df["is_pha"]) & (df["min_miss_distance_km"] < 0.05 * AU_IN_KM),
    ]
    df["threat_level"] = np.select(conditions, [3, 2, 1], default=0)
    return df