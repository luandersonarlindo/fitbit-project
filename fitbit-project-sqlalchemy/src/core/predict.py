import pickle
import pandas as pd

def predict_from_pickle(pickle_path: str, df_spec: pd.DataFrame):
    with open(pickle_path, "rb") as f:
        model = pickle.load(f)
    features = ["total_steps","total_distance_km","mvpa_minutes","active_minutes","sedentary_minutes","steps_per_km"]
    X = df_spec[features].fillna(0)
    yhat = model.predict(X)
    return yhat
