import streamlit as st
import pandas as pd
from core.db import create_database, exec_sql_files
from core.etl import load_csv_to_sor, transform_to_sot, transform_to_spec
from core.train import train_and_save
from core.predict import predict_from_pickle

st.title("Fitbit Project - Predição de Calorias")

option = st.radio("Escolha a opção:", ("Treinar modelo", "Usar modelo salvo (.pickle)"))

engine_url = "sqlite:///fitbit.db"
csv_path = "dailyActivity_merged.csv"

if option == "Treinar modelo":
    st.write("Rodando pipeline completo...")
    engine = create_database(engine_url)
    exec_sql_files(engine)
    load_csv_to_sor(engine, csv_path)
    transform_to_sot(engine)
    transform_to_spec(engine)
    model_path, metrics = train_and_save(engine)
    st.success(f"Modelo treinado e salvo em {model_path}")
    st.json(metrics)

else:
    st.write("Carregando modelo salvo...")
    engine = create_database(engine_url)
    exec_sql_files(engine)
    load_csv_to_sor(engine, csv_path)
    transform_to_sot(engine)
    transform_to_spec(engine)
    df_spec = pd.read_sql("SELECT * FROM spec_activity_features", engine)
    preds = predict_from_pickle("model/calories_regression.pickle", df_spec)
    st.write("Exemplo de previsões:", preds[:10])
