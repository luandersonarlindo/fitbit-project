"""
Arquivo principal para executar o aplicativo Streamlit
"""
import os
import sys
import subprocess

# Adiciona o diretório do projeto ao path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SRC_DIR)

def run_streamlit():
    """Executa o aplicativo Streamlit"""
    app_path = os.path.join(SRC_DIR, "app.py")
    
    print("🚀 Iniciando Fitbit Project - Predição de Calorias")
    print(f"📁 Executando: {app_path}")
    print("🌐 O aplicativo será aberto em: http://localhost:8501")
    print("⏹️ Para parar: Ctrl+C no terminal")
    print("-" * 50)
    
    # Configura o diretório de trabalho para src
    os.chdir(SRC_DIR)
    
    # Executa o Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

def run_pipeline():
    """Executa o pipeline via CLI"""
    sys.path.insert(0, SRC_DIR)
    
    from main_app import run_pipeline
    
    # Caminhos corretos para execução a partir da raiz
    db_path = os.path.join(PROJECT_ROOT, "database", "fitbit.db")
    csv_path = os.path.join(PROJECT_ROOT, "data", "dailyActivity_merged.csv")
    engine_url = f"sqlite:///{db_path}"
    
    print("⚙️ Executando pipeline completo...")
    print(f"📊 CSV: {csv_path}")
    print(f"🗄️ Database: {db_path}")
    
    model_path, metrics = run_pipeline(engine_url, csv_path)
    print(f"✅ Modelo treinado e salvo em: {model_path}")
    print("📊 Métricas:")
    for split, values in metrics.items():
        print(f"  {split.upper()}:")
        for metric, value in values.items():
            print(f"    {metric.upper()}: {value:.4f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fitbit Project Runner")
    parser.add_argument("--mode", choices=["web", "cli"], default="web", 
                       help="Modo de execução: web (Streamlit) ou cli (pipeline)")
    
    args = parser.parse_args()
    
    if args.mode == "web":
        run_streamlit()
    else:
        run_pipeline()
