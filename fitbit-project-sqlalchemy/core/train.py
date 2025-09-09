import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

def train_and_save(engine, model_path="model/calories_regression.pickle"):
    df = pd.read_sql("SELECT * FROM spec_activity_features", engine)
    features = ["total_steps","total_distance_km","mvpa_minutes","active_minutes","sedentary_minutes","steps_per_km"]
    X = df[features].fillna(0)
    y = df["calories"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    metrics = {
        "train": {
            "r2": r2_score(y_train, model.predict(X_train)),
            "mae": mean_absolute_error(y_train, model.predict(X_train))
        },
        "valid": {
            "r2": r2_score(y_val, model.predict(X_val)),
            "mae": mean_absolute_error(y_val, model.predict(X_val))
        }
    }

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    return model_path, metrics
