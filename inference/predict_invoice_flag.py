import joblib
import pandas as pd


MODEL_PATH = "models/predict_flag_invoice.pkl"
BASE_INVOICE_FEATURES = [
    "invoice_quantity",
    "invoice_amount_inr",
    "freight_inr",
    "total_item_quantity",
    "total_item_amount_inr",
]
INVOICE_FEATURES = BASE_INVOICE_FEATURES + [
    "amount_gap_inr",
    "quantity_gap",
    "freight_ratio",
]


def load_model(model_path: str = MODEL_PATH):
    with open(model_path, "rb") as f:
        return joblib.load(f)


def _prepare_features(input_df: pd.DataFrame) -> pd.DataFrame:
    df = input_df.rename(
        columns={
            "invoice_dollars": "invoice_amount_inr",
            "Dollars": "invoice_amount_inr",
            "Freight": "freight_inr",
            "total_item_dollars": "total_item_amount_inr",
        }
    ).copy()

    missing = sorted(set(BASE_INVOICE_FEATURES) - set(df.columns))
    if missing:
        raise ValueError(f"Missing invoice review fields: {missing}")

    df["amount_gap_inr"] = (
        df["invoice_amount_inr"] - df["total_item_amount_inr"]
    ).abs()
    df["quantity_gap"] = (
        df["invoice_quantity"] - df["total_item_quantity"]
    ).abs()
    df["freight_ratio"] = (
        df["freight_inr"] / df["invoice_amount_inr"].replace(0, pd.NA)
    ).fillna(0)
    return df[INVOICE_FEATURES]


def predict_invoice_flag(input_data):
    """
    Predict whether an India invoice should be held for manual review.
    """
    model = load_model()
    input_df = pd.DataFrame(input_data)
    features = _prepare_features(input_df)
    output = input_df.copy()
    output["Predicted_Flag"] = model.predict(features)
    output["Flag_Probability"] = model.predict_proba(features)[:, 1]
    return output


if __name__ == "__main__":
    sample_data = {
        "invoice_quantity": [5, 5],
        "invoice_amount_inr": [1200, 1200],
        "freight_inr": [950, 950],
        "total_item_quantity": [5, 2],
        "total_item_amount_inr": [1190, 800],
    }
    print(predict_invoice_flag(sample_data))
