# 📋 RESUMO TÉCNICO DOS ARQUIVOS

> **📚 Documentação Completa**: Veja o [README.md](README.md) para informações detalhadas sobre instalação, uso e arquitetura.

## 🎯 Arquivos Principais

### 🖥️ `app.py` - Interface Streamlit
**Funcionalidades:**
- Interface web interativa para o projeto
- Opção 1: **Treinar modelo** - Pipeline completo de ETL + ML
- Opção 2: **Usar modelo salvo** - Predições com modelo existente
- Visualização de métricas (R², MAE) e estatísticas
- Tratamento robusto de erros (PermissionError, modelo inexistente)

### ⚙️ `main_app.py` - Pipeline CLI
**Funcionalidades:**
- Execução via linha de comando sem interface gráfica
- Pipeline automatizado: DB → ETL → Treinamento
- Retorna caminho do modelo e métricas de performance
- Ideal para automação e scripts

## 🗂️ Módulos Core

### 🗄️ `core/db.py` - Gestão de Database
**Funcionalidades:**
- `create_database()`: Cria SQLite com tratamento de PermissionError
- `exec_sql_files()`: Executa scripts SQL automaticamente
- Gestão robusta de conexões e cleanup

### 🔄 `core/etl.py` - Pipeline ETL
**Funcionalidades:**
- `load_csv_to_sor()`: Ingestão de dados brutos do CSV
- `transform_to_sot()`: Limpeza e padronização (SOR → SOT)  
- `transform_to_spec()`: Feature engineering (SOT → SPEC)
- Conversão de datas e criação de variáveis derivadas

### 🤖 `core/train.py` - Machine Learning
**Funcionalidades:**
- `train_and_save()`: Treinamento de regressão linear
- Split treino/validação (80/20)
- Cálculo de métricas (R², MAE)
- Serialização do modelo em `.pickle`

### 🔮 `core/predict.py` - Predições
**Funcionalidades:**
- `predict_from_pickle()`: Carrega modelo salvo
- Aplicação de predições em DataFrames
- Tratamento de valores ausentes (fillna)

## 📊 Dados e Schemas

### 📁 `core/data/*.sql` - Definições de Tabelas
- `sor_daily_activity.sql`: Schema para dados brutos
- `sot_daily_activity.sql`: Schema para dados tratados  
- `spec_activity_features.sql`: Schema para features de ML

### 📈 `dailyActivity_merged.csv` - Dataset
- Dados originais de atividades do Fitbit
- ~940 registros de usuários únicos
- Métricas: passos, distância, minutos ativos, calorias

## 📋 Documentação Adicional

### 🏗️ `architecture.md` - Diagramas Técnicos
- Fluxogramas do pipeline de dados
- Representação visual das transformações
- Mapeamento SOR → SOT → SPEC

### 📚 `data_model.md` - Especificação Detalhada
- Definições completas de cada tabela
- Tipos de dados e constraints
- Relacionamentos e chaves primárias

---

## 🎯 **Próximos Passos**

1. **📖 Leia**: [README.md](README.md) para setup completo
2. **▶️ Execute**: `streamlit run app.py` para interface web
3. **🔧 Desenvolva**: Consulte documentação técnica para customizações
