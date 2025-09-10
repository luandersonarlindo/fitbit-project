import os
import glob
import time
from sqlalchemy import create_engine, text

def create_database(engine_url="sqlite:///fitbit.db"):
    if engine_url.startswith("sqlite:///"):
        db_path = engine_url.replace("sqlite:///", "")
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except PermissionError:
                # Se não conseguir remover, tenta usar um nome alternativo
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_db_path = f"fitbit_{timestamp}.db"
                engine_url = f"sqlite:///{new_db_path}"
            except Exception as e:
                print(f"Aviso: Não foi possível remover o banco existente: {e}")
                # Continua com o banco existente
    
    engine = create_engine(engine_url, future=True)
    return engine

def exec_sql_files(engine, folder="core/data"):
    with engine.begin() as conn:
        for sql_file in sorted(glob.glob(f"{folder}/*.sql")):
            with open(sql_file, "r", encoding="utf-8") as f:
                conn.execute(text(f.read()))
