import streamlit as st
import pandas as pd
import os
from core.db import create_database, exec_sql_files
from core.etl import load_csv_to_sor, transform_to_sot, transform_to_spec
from core.train import train_and_save
from core.predict import predict_from_pickle

st.title("Fitbit Project - Predição de Calorias")

option = st.radio("Escolha a opção:", ("Treinar modelo", "Usar modelo salvo (.pickle)"))

engine_url = "sqlite:///fitbit.db"
csv_path = "dailyActivity_merged.csv"

if option == "Treinar modelo":
    st.write("🔄 Rodando pipeline completo...")
    
    try:
        engine = create_database(engine_url)
        exec_sql_files(engine)
        load_csv_to_sor(engine, csv_path)
        transform_to_sot(engine)
        transform_to_spec(engine)
        model_path, metrics = train_and_save(engine)
        st.success(f"✅ Modelo treinado e salvo em {model_path}")
        st.json(metrics)
    except Exception as e:
        st.error(f"❌ Erro durante o treinamento: {str(e)}")
        st.info("💡 Tente fechar outras conexões com o banco de dados ou reinicie o aplicativo.")

else:
    st.write("📁 Carregando modelo salvo...")
    
    # Verifica se o modelo existe
    if not os.path.exists("model/calories_regression.pickle"):
        st.error("❌ Modelo não encontrado! Execute o treinamento primeiro.")
        st.info("👆 Selecione 'Treinar modelo' acima para criar o modelo.")
    else:
        try:
            # Verifica se o banco já existe e tem dados
            if os.path.exists("fitbit.db"):
                from sqlalchemy import create_engine
                engine = create_engine(engine_url, future=True)
                
                # Tenta verificar se as tabelas existem
                try:
                    df_spec = pd.read_sql("SELECT * FROM spec_activity_features LIMIT 1", engine)
                    # Se chegou até aqui, os dados já existem
                    st.info("🔄 Usando dados existentes do banco...")
                    df_spec = pd.read_sql("SELECT * FROM spec_activity_features", engine)
                except:
                    # Precisa processar os dados
                    st.info("📊 Processando dados para previsão...")
                    exec_sql_files(engine)
                    load_csv_to_sor(engine, csv_path)
                    transform_to_sot(engine)
                    transform_to_spec(engine)
                    df_spec = pd.read_sql("SELECT * FROM spec_activity_features", engine)
            else:
                # Banco não existe, precisa criar
                st.info("🏗️ Criando banco e processando dados...")
                engine = create_database(engine_url)
                exec_sql_files(engine)
                load_csv_to_sor(engine, csv_path)
                transform_to_sot(engine)
                transform_to_spec(engine)
                df_spec = pd.read_sql("SELECT * FROM spec_activity_features", engine)
            
            # Fazer previsões
            preds = predict_from_pickle("model/calories_regression.pickle", df_spec)
            
            st.success("✅ Previsões concluídas!")
            st.write(f"📊 Total de registros processados: {len(preds)}")
            st.write("🔮 Primeiras 10 previsões de calorias:", preds[:10])
            
            # Mostrar estatísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mínimo", f"{preds.min():.0f}")
            with col2:
                st.metric("Média", f"{preds.mean():.0f}")
            with col3:
                st.metric("Máximo", f"{preds.max():.0f}")
                
        except Exception as e:
            st.error(f"❌ Erro ao fazer previsões: {str(e)}")
            st.info("💡 Tente reiniciar o aplicativo ou execute o treinamento novamente.")
