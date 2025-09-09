from core.db import create_database, exec_sql_files
from core.etl import load_csv_to_sor, transform_to_sot, transform_to_spec
from core.train import train_and_save

def run_pipeline(engine_url="sqlite:///fitbit.db", csv_path="dailyActivity_merged.csv"):
    engine = create_database(engine_url)
    exec_sql_files(engine)
    load_csv_to_sor(engine, csv_path)
    transform_to_sot(engine)
    transform_to_spec(engine)
    model_path, metrics = train_and_save(engine)
    return model_path, metrics
