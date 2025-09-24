# src/core/models.py
import pickle
from pathlib import Path
from sklearn.linear_model import LinearRegression
import pandas as pd

MODEL_PATH = Path(__file__).parents[1] / "model" / "calories_regression.pickle"

def train():
    """
    Treina um modelo de regressão linear simples com dados fictícios.
    Salva o modelo em MODEL_PATH.
    """
    # Dados de exemplo (substitua pelos dados reais do Fitbit)
    data = pd.DataFrame({
        "TotalSteps": [5000, 8000, 10000, 12000],
        "VeryActiveMinutes": [20, 30, 50, 60],
        "FairlyActiveMinutes": [10, 20, 30, 40],
        "LightlyActiveMinutes": [60, 50, 40, 30],
        "SedentaryMinutes": [600, 550, 500, 450],
        "Distance": [4.0, 6.5, 8.0, 9.5],
        "Calories": [2000, 2300, 2500, 2800]
    })

    X = data.drop("Calories", axis=1)
    y = data["Calories"]

    model = LinearRegression()
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

def predict_from_row(features: dict) -> float:
    """
    Recebe um dicionário com as features e retorna a previsão de calorias.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Modelo não encontrado. Treine primeiro.")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    return prediction
