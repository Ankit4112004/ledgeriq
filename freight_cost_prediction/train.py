import json
from pathlib import Path

import joblib

from data_preprocessing import FREIGHT_FEATURES, load_india_freight_data, prepare_features, split_data
from modeling_evaluation import (
    evaluate_model,
    train_gradient_boosting,
    train_random_forest,
    train_ridge,
)


def main():
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    df = load_india_freight_data()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    models = {
        "Ridge Regression": train_ridge(X_train, y_train),
        "Gradient Boosting Regression": train_gradient_boosting(X_train, y_train),
        "Random Forest Regression": train_random_forest(X_train, y_train),
    }

    results = [
        evaluate_model(model, X_test, y_test, model_name)
        for model_name, model in models.items()
    ]

    best_model_info = min(results, key=lambda item: item["mae"])
    best_model_name = best_model_info["model_name"]
    best_model = models[best_model_name]

    model_path = model_dir / "predict_freight_model.pkl"
    metadata_path = model_dir / "predict_freight_model_metadata.json"
    joblib.dump(best_model, model_path)

    metadata = {
        "country": "India",
        "currency": "INR",
        "dataset": "Delivery Logistics Dataset (India - Multi-Partner)",
        "training_rows": int(len(df)),
        "features": FREIGHT_FEATURES,
        "target": "delivery_cost",
        "best_model": best_model_name,
        "metrics": best_model_info,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"\nBest model saved: {best_model_name}")
    print(f"Model path: {model_path}")
    print(f"Metadata path: {metadata_path}")


if __name__ == "__main__":
    main()
