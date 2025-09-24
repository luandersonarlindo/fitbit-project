import os
import glob
import time
from sqlalchemy import create_engine, text

def create_database(engine_url="sqlite:///fitbit.db"):
    if engine_url.startswith("sqlite:///"):
        db_path = engine_url.replace("sqlite:///", "")
        
        # Se for caminho relativo, converte para absoluto
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)
        
        # Cria diretório se não existir
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except PermissionError:
                # Se não conseguir remover, tenta usar um nome alternativo
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_db_path = os.path.join(db_dir, f"fitbit_{timestamp}.db")
                engine_url = f"sqlite:///{new_db_path}"
            except Exception as e:
                print(f"Aviso: Não foi possível remover o banco existente: {e}")
                # Continua com o banco existente
        else:
            # Atualiza a URL com o caminho absoluto
            engine_url = f"sqlite:///{db_path}"
    
    engine = create_engine(engine_url, future=True)
    return engine

def exec_sql_files(engine, folder="core/data"):
    # Se for caminho relativo, converte para absoluto
    if not os.path.isabs(folder):
        folder = os.path.abspath(folder)
    
    print(f"Procurando arquivos SQL em: {folder}")
    
    with engine.begin() as conn:
        sql_files = sorted(glob.glob(f"{folder}/*.sql"))
        print(f"Arquivos SQL encontrados: {sql_files}")
        
        for sql_file in sql_files:
            print(f"Executando: {os.path.basename(sql_file)}")
            with open(sql_file, "r", encoding="utf-8") as f:
                conn.execute(text(f.read()))
