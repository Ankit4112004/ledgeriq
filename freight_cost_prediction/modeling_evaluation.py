from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = ["distance_km", "package_weight_kg"]
CATEGORICAL_FEATURES = [
    "delivery_mode",
    "vehicle_type",
    "package_type",
    "region",
    "weather_condition",
]


def build_pipeline(model):
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def train_ridge(X_train, y_train):
    model = Ridge(alpha=1.0)
    pipe = build_pipeline(model)
    pipe.fit(X_train, y_train)
    return pipe


def train_gradient_boosting(X_train, y_train):
    model = GradientBoostingRegressor(
        n_estimators=180,
        learning_rate=0.06,
        max_depth=4,
        random_state=42,
    )
    pipe = build_pipeline(model)
    pipe.fit(X_train, y_train)
    return pipe


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=180,
        max_depth=14,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )
    pipe = build_pipeline(model)
    pipe.fit(X_train, y_train)
    return pipe


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds) * 100

    print(f"\n{model_name} Performance:")
    print(f"MAE  : INR {mae:.2f}")
    print(f"RMSE : INR {rmse:.2f}")
    print(f"R2   : {r2:.2f}%")

    return {
        "model_name": model_name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }
