import os
import glob
from sqlalchemy import create_engine, text

def create_database(engine_url="sqlite:///fitbit.db"):
    if engine_url.startswith("sqlite:///"):
        db_path = engine_url.replace("sqlite:///", "")
        if os.path.exists(db_path):
            os.remove(db_path)
    engine = create_engine(engine_url, future=True)
    return engine

def exec_sql_files(engine, folder="core/data"):
    with engine.begin() as conn:
        for sql_file in sorted(glob.glob(f"{folder}/*.sql")):
            with open(sql_file, "r", encoding="utf-8") as f:
                conn.execute(text(f.read()))
