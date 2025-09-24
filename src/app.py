import streamlit as st
from pathlib import Path
import sys

# Ajustar import para módulos locais
sys.path.append(str(Path(__file__).resolve().parents[0]))

from core.models import train, predict_from_row as predict
from core.explain import show_coefficients as coefficients
from core.rules import answer_intent as rules


st.set_page_config(page_title="Fitbit Analytics", page_icon="📊", layout="wide")

st.title("📊 Fitbit Analytics Dashboard")
st.markdown("Bem-vindo ao painel interativo de análise Fitbit!")

menu = st.sidebar.radio(
    "Menu",
    ["🏋️ Treinar Modelo", "📈 Predição de Calorias", "🧮 Coeficientes do Modelo", "🤖 Chatbot Fitbit"]
)

# --------------------- Treinar Modelo ---------------------
if menu == "🏋️ Treinar Modelo":
    st.header("Treinamento do Modelo de Regressão")
    if st.button("Treinar agora"):
        try:
            train()
            st.success("✅ Treinamento concluído e modelo salvo!")
        except Exception as e:
            st.error(f"Erro durante o treinamento: {e}")

# --------------------- Predição de Calorias ---------------------
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
            # Chamada corrigida da função
            result = predict(features)
            st.success(f"🔥 Calorias previstas: {result:.2f}")
        except Exception as e:
            st.error(f"Erro na predição: {e}")

# --------------------- Coeficientes do Modelo ---------------------
elif menu == "🧮 Coeficientes do Modelo":
    st.header("Coeficientes do Modelo de Regressão")
    try:
        # Caminho do modelo
        model_path = Path("../src/model/calories_regression.pickle")
        
        # Carregar o modelo do pickle
        import pickle
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        
        # Obter coeficientes e intercepto
        coefs = {feature: coef for feature, coef in zip(model.feature_names_in_, model.coef_)}
        intercept = model.intercept_
        
        # Exibir no Streamlit
        st.subheader("Intercepto")
        st.write(intercept)
        st.subheader("Coeficientes")
        st.json(coefs)
        
    except Exception as e:
        st.error(f"Erro ao carregar coeficientes: {e}")


# --------------------- Chatbot Fitbit ---------------------
elif menu == "🤖 Chatbot Fitbit":
    st.header("Assistente Fitbit")
    user_input = st.text_input("Digite sua pergunta (ex: 'calorias hoje', 'passos hoje', 'padrões de usuários ativos')")
    if st.button("Responder"):
        intent = None
        if "caloria" in user_input.lower():
            intent = "calories_today"
        elif "passo" in user_input.lower():
            intent = "steps_today"
        elif "minuto" in user_input.lower():
            intent = "active_minutes"
        elif "padrão" in user_input.lower() or "ativo" in user_input.lower():
            intent = "active_patterns"
        else:
            intent = "help"

        # Chamada corrigida da função
        resposta = rules(intent, {"Calories": 2300, "TotalSteps": 8500, "ActiveMinutes": 120})
        st.success(resposta)
