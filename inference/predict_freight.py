import joblib
import pandas as pd


MODEL_PATH = "models/predict_freight_model.pkl"
FREIGHT_FEATURES = [
    "distance_km",
    "package_weight_kg",
    "delivery_mode",
    "vehicle_type",
    "package_type",
    "region",
    "weather_condition",
]


def load_model(model_path: str = MODEL_PATH):
    with open(model_path, "rb") as f:
        return joblib.load(f)


def predict_freight_cost(input_data):
    """
    Predict India delivery/freight cost in INR.
    """
    model = load_model()
    input_df = pd.DataFrame(input_data).copy()
    missing = sorted(set(FREIGHT_FEATURES) - set(input_df.columns))
    if missing:
        raise ValueError(f"Missing freight forecast fields: {missing}")

    for col in ["delivery_mode", "vehicle_type", "package_type", "region", "weather_condition"]:
        input_df[col] = input_df[col].astype(str).str.strip().str.lower()

    input_df["Predicted_Freight_INR"] = model.predict(input_df[FREIGHT_FEATURES]).round(2)
    return input_df


if __name__ == "__main__":
    sample_data = {
        "distance_km": [120],
        "package_weight_kg": [12.5],
        "delivery_mode": ["express"],
        "vehicle_type": ["truck"],
        "package_type": ["electronics"],
        "region": ["west"],
        "weather_condition": ["clear"],
    }
    print(predict_freight_cost(sample_data))
