"""
Configurações de caminhos e parâmetros do projeto
"""
import os

# Diretório raiz do projeto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Caminhos de dados
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CSV_PATH = os.path.join(DATA_DIR, "dailyActivity_merged.csv")

# Caminhos de banco de dados
DATABASE_DIR = os.path.join(PROJECT_ROOT, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "fitbit.db")
ENGINE_URL = f"sqlite:///{DATABASE_PATH}"

# Caminhos de modelos
MODEL_DIR = os.path.join(PROJECT_ROOT, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "calories_regression.pickle")

# Caminhos de documentação
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# Caminhos de notebooks
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, "notebooks")

# Caminhos de código fonte
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
CORE_DATA_SQL_DIR = os.path.join(SRC_DIR, "core", "data")
