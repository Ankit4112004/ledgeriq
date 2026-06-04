from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


FREIGHT_FEATURES = [
    "distance_km",
    "package_weight_kg",
    "delivery_mode",
    "vehicle_type",
    "package_type",
    "region",
    "weather_condition",
]

FREIGHT_TARGET = "delivery_cost"


def load_india_freight_data(
    csv_path: str = "data/india/Delivery_Logistics_India.csv",
) -> pd.DataFrame:
    """
    Load India multi-partner delivery logistics data.

    The Kaggle dataset is India-oriented and contains delivery cost, distance,
    weight, delivery mode, vehicle type, package type, region, and weather.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"India freight dataset not found at {path}. "
            "Run the dataset import step or place Delivery_Logistics_India.csv there."
        )

    df = pd.read_csv(path)
    required = FREIGHT_FEATURES + [FREIGHT_TARGET]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required freight columns: {missing}")

    df = df[required].copy()
    for col in ["distance_km", "package_weight_kg", FREIGHT_TARGET]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["delivery_mode", "vehicle_type", "package_type", "region", "weather_condition"]:
        df[col] = df[col].astype(str).str.strip().str.lower()

    df = df.dropna()
    df = df[
        (df["distance_km"] > 0)
        & (df["package_weight_kg"] > 0)
        & (df[FREIGHT_TARGET] > 0)
    ]
    return df.reset_index(drop=True)


def prepare_features(df: pd.DataFrame):
    X = df[FREIGHT_FEATURES]
    y = df[FREIGHT_TARGET]
    return X, y


def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
