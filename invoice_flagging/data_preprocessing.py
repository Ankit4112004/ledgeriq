from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


BASE_INVOICE_FEATURES = [
    "invoice_quantity",
    "invoice_amount_inr",
    "freight_inr",
    "total_item_quantity",
    "total_item_amount_inr",
]

DERIVED_INVOICE_FEATURES = [
    "amount_gap_inr",
    "quantity_gap",
    "freight_ratio",
]

INVOICE_FEATURES = BASE_INVOICE_FEATURES + DERIVED_INVOICE_FEATURES
TARGET = "flag_invoice"


def _add_review_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["amount_gap_inr"] = (
        df["invoice_amount_inr"] - df["total_item_amount_inr"]
    ).abs()
    df["quantity_gap"] = (
        df["invoice_quantity"] - df["total_item_quantity"]
    ).abs()
    df["freight_ratio"] = (
        df["freight_inr"] / df["invoice_amount_inr"].replace(0, np.nan)
    ).fillna(0)
    return df


def load_invoice_data(csv_path: str = "data/india/DTDC_Courier_India.csv") -> pd.DataFrame:
    """
    Build an India invoice-review training table from the DTDC courier dataset.

    Public India PO-to-vendor-invoice datasets are scarce because they contain
    sensitive GSTIN/vendor/payment data. This derives a supervised review set
    from real/synthetic India courier invoice charges, then injects controlled
    PO/GRN mismatches to train the classifier on the reconciliation behavior.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"India courier invoice dataset not found at {path}. "
            "Run the dataset import step or place DTDC_Courier_India.csv there."
        )

    raw = pd.read_csv(path)
    required = ["Total Pieces", "Total Amount", "Tariff"]
    missing = sorted(set(required) - set(raw.columns))
    if missing:
        raise ValueError(f"Missing required invoice columns: {missing}")

    df = raw[required].copy()
    df["invoice_quantity"] = pd.to_numeric(df["Total Pieces"], errors="coerce")
    df["invoice_amount_inr"] = pd.to_numeric(df["Total Amount"], errors="coerce")
    df["freight_inr"] = pd.to_numeric(df["Tariff"], errors="coerce")
    df = df.dropna()
    df = df[
        (df["invoice_quantity"] > 0)
        & (df["invoice_amount_inr"] > 0)
        & (df["freight_inr"] > 0)
    ][["invoice_quantity", "invoice_amount_inr", "freight_inr"]]

    rng = np.random.default_rng(42)
    n = len(df)
    risk_mask = rng.random(n) < 0.38

    df["total_item_quantity"] = df["invoice_quantity"].astype(int)
    clean_noise = rng.uniform(-30, 30, n)
    df["total_item_amount_inr"] = (df["invoice_amount_inr"] + clean_noise).clip(lower=1)
    df[TARGET] = 0

    risky_idx = np.where(risk_mask)[0]
    amount_risk = rng.random(len(risky_idx)) < 0.75

    amount_idx = risky_idx[amount_risk]
    if len(amount_idx):
        direction = rng.choice([-1, 1], len(amount_idx))
        percent_gap = rng.uniform(0.06, 0.28, len(amount_idx))
        flat_gap = rng.uniform(75, 750, len(amount_idx))
        gap = df.iloc[amount_idx]["invoice_amount_inr"].to_numpy() * percent_gap + flat_gap
        changed_amount = np.clip(
            df.iloc[amount_idx]["invoice_amount_inr"].to_numpy() + direction * gap,
            1,
            None,
        )
        df.iloc[
            amount_idx,
            df.columns.get_loc("total_item_amount_inr"),
        ] = changed_amount

    quantity_idx = risky_idx[~amount_risk]
    if len(quantity_idx):
        qty_gap = rng.integers(1, 4, len(quantity_idx))
        direction = rng.choice([-1, 1], len(quantity_idx))
        changed_qty = np.clip(
            df.iloc[quantity_idx]["invoice_quantity"].to_numpy() + direction * qty_gap,
            1,
            None,
        )
        df.iloc[
            quantity_idx,
            df.columns.get_loc("total_item_quantity"),
        ] = changed_qty

    df.iloc[risky_idx, df.columns.get_loc(TARGET)] = 1
    df = _add_review_features(df)
    return df[INVOICE_FEATURES + [TARGET]].reset_index(drop=True)


def prepare_inference_features(input_df: pd.DataFrame) -> pd.DataFrame:
    renamed = input_df.rename(
        columns={
            "invoice_dollars": "invoice_amount_inr",
            "Dollars": "invoice_amount_inr",
            "Freight": "freight_inr",
            "total_item_dollars": "total_item_amount_inr",
        }
    ).copy()
    missing = sorted(set(BASE_INVOICE_FEATURES) - set(renamed.columns))
    if missing:
        raise ValueError(f"Missing invoice review fields: {missing}")
    return _add_review_features(renamed)[INVOICE_FEATURES]


def split_data(df, features=INVOICE_FEATURES, target=TARGET):
    X = df[features]
    y = df[target]
    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
