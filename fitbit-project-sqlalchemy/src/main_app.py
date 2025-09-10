from core.db import create_database, exec_sql_files
from core.etl import load_csv_to_sor, transform_to_sot, transform_to_spec
from core.train import train_and_save

def run_pipeline(engine_url="sqlite:///../database/fitbit.db", csv_path="../data/dailyActivity_merged.csv"):
    import os
    
    engine = create_database(engine_url)
    
    # Caminho correto para os arquivos SQL
    sql_folder = os.path.join(os.path.dirname(__file__), "core", "data")
    exec_sql_files(engine, sql_folder)
    
    load_csv_to_sor(engine, csv_path)
    transform_to_sot(engine)
    transform_to_spec(engine)
    # Caminho correto para salvar o modelo
    model_path = os.path.join(os.path.dirname(__file__), "..", "model", "calories_regression.pickle")
    model_path, metrics = train_and_save(engine, model_path)
    return model_path, metrics
