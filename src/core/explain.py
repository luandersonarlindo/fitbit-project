# src/core/explain.py
import pickle
from pathlib import Path

def show_coefficients(model_path: Path):
    """
    Exibe os coeficientes do modelo de regressão linear.
    """
    if not model_path.exists():
        raise FileNotFoundError("Modelo não encontrado.")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("Coeficientes do modelo:")
    for feature, coef in zip(model.feature_names_in_, model.coef_):
        print(f"{feature}: {coef:.4f}")

    print(f"Intercepto: {model.intercept_:.4f}")
