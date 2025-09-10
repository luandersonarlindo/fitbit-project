# RESUMO DOS ARQUIVOS DO PROJETO FITBIT

## app.py
Arquivo principal da interface web (usando Streamlit). Permite ao usuário:
- Treinar o modelo de regressão linear para previsão de calorias, executando todo o pipeline de ETL e treinamento.
- Usar um modelo já salvo para fazer previsões com base nos dados processados.
- Mostra métricas do modelo treinado e exemplos de previsões.

## main_app.py
Script Python para execução do pipeline completo via linha de comando (sem interface gráfica):
- Cria o banco de dados SQLite e as tabelas.
- Executa o ETL: carrega o CSV, transforma dados e gera features.
- Treina o modelo e salva o arquivo `.pickle`.
- Retorna o caminho do modelo e métricas de avaliação.

## README.md
Arquivo de documentação inicial do projeto. Geralmente contém instruções de uso, objetivos e informações gerais (o conteúdo está vazio ou incompleto neste momento).

## architecture.md
Documento que descreve a arquitetura do pipeline:
- Mostra o fluxo de dados do CSV até o modelo salvo.
- Explica as zonas de dados (SOR, SOT, SPEC) e o papel de cada etapa.
- Resume o funcionamento do pipeline executado pelo `main_app.py`.

## data_model.md
Descreve detalhadamente o modelo de dados do projeto:
- Explica as três zonas: SOR (dados brutos), SOT (dados tratados) e SPEC (features para modelagem).
- Lista as tabelas, colunas, tipos e chaves primárias de cada zona.
- Serve como referência para o entendimento do banco de dados e do processo de ETL.

## core/db.py
Funções utilitárias para manipulação do banco de dados:
- Criação do banco SQLite (removendo o antigo, se existir).
- Execução automática dos scripts SQL para criar as tabelas.

## core/etl.py
Implementa o pipeline ETL:
- Carrega o CSV para a tabela SOR, convertendo datas e renomeando colunas.
- Transforma dados da SOR para a SOT (tratamento e padronização).
- Gera a tabela SPEC com as features finais para modelagem.

## core/predict.py
Função para realizar previsões usando um modelo salvo (`.pickle`):
- Carrega o modelo de regressão linear.
- Recebe um DataFrame de features e retorna as previsões de calorias.

## core/train.py
Função para treinar e salvar o modelo de regressão linear:
- Lê os dados da tabela SPEC.
- Separa treino e validação.
- Treina o modelo, calcula métricas (R², MAE) e salva o modelo em arquivo `.pickle`.

---

**Observação:**
- O projeto segue boas práticas de engenharia de dados, separando zonas de dados e modularizando o código.
- O pipeline pode ser executado tanto via interface web (app.py) quanto por script (main_app.py).
- Os arquivos SQL em `core/data/` criam as tabelas do banco.
- O modelo treinado é salvo em `model/calories_regression.pickle`.
