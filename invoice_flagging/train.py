import json
from pathlib import Path

import joblib

from data_preprocessing import INVOICE_FEATURES, TARGET, load_invoice_data, split_data
from modeling_evaluation import evaluate_classifier, train_random_forest


def main():
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    df = load_invoice_data()
    X_train, X_test, y_train, y_test = split_data(df, INVOICE_FEATURES, TARGET)

    model = train_random_forest(X_train, y_train)
    metrics = evaluate_classifier(
        model,
        X_test,
        y_test,
        "India Invoice Review Random Forest",
    )

    model_path = model_dir / "predict_flag_invoice.pkl"
    metadata_path = model_dir / "predict_flag_invoice_metadata.json"
    joblib.dump(model, model_path)

    metadata = {
        "country": "India",
        "currency": "INR",
        "dataset": "DTDC Courier Dataset",
        "training_rows": int(len(df)),
        "features": INVOICE_FEATURES,
        "target": TARGET,
        "model": metrics["model_name"],
        "metrics": metrics,
        "label_note": (
            "Labels are derived by injecting controlled PO/GRN amount and "
            "quantity mismatches around India courier invoice charges."
        ),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"\nModel path: {model_path}")
    print(f"Metadata path: {metadata_path}")


if __name__ == "__main__":
    main()
