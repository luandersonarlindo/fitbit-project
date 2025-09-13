import streamlit as st
from pathlib import Path
import sys

# Ajustar import para módulos locais
sys.path.append(str(Path(__file__).resolve().parents[0]))

from core.models import train, predict
from core.explain import coefficients
from core.chatbot import rules

st.set_page_config(page_title="Fitbit Analytics", page_icon="📊", layout="wide")

st.title("📊 Fitbit Analytics Dashboard")
st.markdown("Bem-vindo ao painel interativo de análise Fitbit!")

menu = st.sidebar.radio("Menu", ["🏋️ Treinar Modelo", "📈 Predição de Calorias", "🧮 Coeficientes do Modelo", "🤖 Chatbot Fitbit"])

if menu == "🏋️ Treinar Modelo":
    st.header("Treinamento do Modelo de Regressão")
    if st.button("Treinar agora"):
        try:
            train.train()
            st.success("✅ Treinamento concluído e modelo salvo!")
        except Exception as e:
            st.error(f"Erro durante o treinamento: {e}")

elif menu == "📈 Predição de Calorias":
    st.header("Faça uma previsão de calorias queimadas")
    steps = st.number_input("Passos totais", min_value=0, value=8000)
    very_active = st.number_input("Minutos muito ativos", min_value=0, value=30)
    fairly_active = st.number_input("Minutos moderadamente ativos", min_value=0, value=20)
    lightly_active = st.number_input("Minutos levemente ativos", min_value=0, value=60)
    sedentary = st.number_input("Minutos sedentários", min_value=0, value=600)
    distance = st.number_input("Distância percorrida (km)", min_value=0.0, value=6.5, format="%.2f")

    if st.button("Prever"):
        try:
            features = {
                "TotalSteps": steps,
                "VeryActiveMinutes": very_active,
                "FairlyActiveMinutes": fairly_active,
                "LightlyActiveMinutes": lightly_active,
                "SedentaryMinutes": sedentary,
                "Distance": distance
            }
            result = predict.predict_from_row(features)
            st.success(f"🔥 Calorias previstas: {result:.2f}")
        except Exception as e:
            st.error(f"Erro na predição: {e}")

elif menu == "🧮 Coeficientes do Modelo":
    st.header("Coeficientes do Modelo de Regressão")
    try:
        model_path = Path(__file__).parents[1] / "model" / "calories_regression.pickle"
        coefficients.show_coefficients(model_path)
        st.info("Coeficientes exibidos no console.")
        st.write("Abra o terminal/logs do Streamlit para visualizar os coeficientes detalhados.")
    except Exception as e:
        st.error(f"Erro ao carregar coeficientes: {e}")

elif menu == "🤖 Chatbot Fitbit":
    st.header("Assistente Fitbit")
    user_input = st.text_input("Digite sua pergunta (ex: 'calorias hoje', 'passos hoje')")
    if st.button("Responder"):
        intent = None
        if "caloria" in user_input.lower():
            intent = "calories_today"
        elif "passo" in user_input.lower():
            intent = "steps_today"
        elif "minuto" in user_input.lower():
            intent = "active_minutes"
        elif "ajuda" in user_input.lower():
            intent = "help"
        else:
            intent = "help"

        resposta = rules.answer_intent(intent, {"Calories": 2300, "TotalSteps": 8500, "ActiveMinutes": 120})
        st.success(resposta)
