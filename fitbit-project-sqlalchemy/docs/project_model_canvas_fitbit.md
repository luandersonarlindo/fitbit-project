# Project Model Canvas — Fitbit

## Contexto
A análise de dados pessoais de atividade (Fitbit) permite extrair insights sobre comportamento físico, padrões de sono e gasto calórico. Esses insights ajudam em recomendações personalizadas, monitoramento de saúde e suporte a decisões (ex.: metas de atividade, intervenções). No repositório enviado há dados históricos (`database/fitbit.db` e `fitbit-project-sqlalchemy/data/dailyActivity_merged.csv`) que contêm registros diários de atividades por usuário.

## Problema a ser Respondido
Como variáveis de atividade diária (passos, distância, minutos ativos, calorias, etc.) e características temporais influenciam indicadores de saúde/atividade (ex.: nível de atividade diária ou calorias gastas)? Podemos prever com precisão útil o nível de atividade (ou outra métrica alvo) para um dia futuro ou para uma pessoa específica?

## Pergunta Norteadora
Quais características mais impactam o indicador alvo selecionado (ex.: `Calories`, `TotalSteps`, `VeryActiveMinutes`)?

- Exemplos: passos totais, minutos ativos por intensidade, dia da semana, índice de sono (se disponível), histórico recente.
- Podemos treinar um modelo de regressão (ou modelo de séries temporais) que gere previsões acionáveis para usuários ou equipes de saúde?

## Objetivos
1. Exploratória: entender distribuição e correlações entre variáveis de atividade.
2. Preditivo: treinar modelos que prevejam o objetivo escolhido (ex.: calorias gastas no dia) com métricas claras (RMSE, MAE, R², erro percentual).
3. Explicável: apresentar importância das features (coeficientes de regressão, SHAP ou permutações).
4. Interativo: construir um chatbot em Streamlit que responda perguntas sobre o treino, explique resultados e gere previsões a partir de novos dados.
5. Reprodutível: pipeline modular, armazenamento do modelo (`.pickle`), e notebooks de análise.

## Solução Proposta
Desenvolver uma aplicação em Streamlit que: 

- Permita o upload ou seleção dos dados existentes (`dailyActivity_merged.csv` / `fitbit.db`).
- Realize ETL e engenharia de features (agregados móveis, indicadores semanais, variáveis dummies para dia da semana, lag features).
- Treine modelos de regressão (Regressão Linear, Random Forest, XGBoost — opcional) e modele séries temporais se necessário.
- Exiba métricas de avaliação (RMSE, MAE, R² e Erro Percentual médio).
- Mostre importância das variáveis (coeficientes + gráficos de contribuição, SHAP quando disponível).
- Chatbot: componente que responde perguntas do usuário sobre o modelo ("Quais as top 5 features?", "Qual a previsão para 2020-03-05 para o usuário X?").
- Permita salvar e carregar modelos treinados para predições rápidas.

## Desenho de Arquitetura
- **Interface (app/)**: Streamlit para upload, visualização dos dados, execução do pipeline, visualização de métricas e interação com chatbot.
- **Core (src/core/)**:
  - `etl.py`: carregamento e limpeza (do CSV e do DB), feature engineering.
  - `train.py`: scripts de treino, seleção de hiperparâmetros e validação cruzada por tempo/usuário.
  - `predict.py`: lógica para inferência em lote ou por instância.
  - `explain.py`: cálculos de importância (coeficientes, SHAP, permutações).
  - `chatbot.py`: interface entre perguntas do usuário e respostas geradas (baseada em FAQ + templates + leitura do modelo/coeficientes).
- **Dados (database/ e data/)**: SOR/SOT/Specs (SQL) para persistência — usar `fitbit.db` como fonte e criar tabelas normalizadas.
- **Modelo (model/)**: armazenar artefatos treinados (`.pkl`, `scaler.pkl`) e versões com metadados (data, métricas)
- **Notebooks (notebooks/)**: EDA, análise de correlação, experimentos de modelos.

## Dados de Entrada (exemplos presentes)
- `dailyActivity_merged.csv` — registros diários com campos típicos: Date, TotalSteps, TotalDistance, VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes, SedentaryMinutes, Calories.
- `fitbit.db` — base SQLite com tabelas históricas que podem complementar os CSVs.

## Variáveis/Features Sugeridas
- Features diretas: `TotalSteps`, `TotalDistance`, `VeryActiveMinutes`, `FairlyActiveMinutes`, `LightlyActiveMinutes`, `SedentaryMinutes`, `Calories` (quando não é alvo), `ActivityDate` => dia/semana/mês.
- Features derivadas: rolling averages (7/14 dias), lags (1/7 dias), razão passos/distância, indicadores de fim de semana, contagem de dias consecutivos ativos.

## Métricas de Avaliação
- RMSE (erro absoluto em unidades do alvo)
- MAE
- R² (coeficiente de determinação)
- Erro Percentual Médio (MAPE ou custom) — cuidado com zeros no denominador
- Pontuação de Acerto (definição: % de previsões dentro de X% do valor real — ex.: ±20%)

## Resultados Esperados
- Modelo baseline (Regressão Linear) com explicabilidade por coeficientes.
- Melhorias com modelos não lineares (ex.: RandomForest) — maior precisão, perda de interpretabilidade.
- Painel Streamlit com:
  - EDA básico (distribuições, correlações)
  - Métricas de avaliação
  - Top features
  - Chatbot interativo que responde perguntas sobre as métricas e o modelo
- Artefato: `submission.csv` (se aplicável) ou arquivo de predições para amostras de validação.

## Plano de Implementação (sprints sugeridos)
1. **Sprint 1 — EDA e ETL (1 semana)**: carregar CSV/DB, limpeza, análise exploratória, definir alvo e features.
2. **Sprint 2 — Pipeline e Baseline (1 semana)**: implementar `etl.py`, `train.py` (linear), validação e métricas.
3. **Sprint 3 — Modelos Avançados e Explicabilidade (1 semana)**: Random Forest / XGBoost, SHAP, feature importance.
4. **Sprint 4 — Streamlit + Chatbot (1 semana)**: construir interface para upload, visualização, inferência e componente de chatbot.
5. **Sprint 5 — Deploy e Documentação (1 semana)**: empacotar app, salvar modelos, publicar no Streamlit Cloud, README no GitHub.

## Recursos Necessários
- Computacional: máquina com Python 3.9+ e bibliotecas (pandas, scikit-learn, xgboost, shap, streamlit).
- Dados: `dailyActivity_merged.csv`, `fitbit.db` (já presentes no repo).
- Pessoal: 1-2 cientistas de dados / engenheiros (p. ex. estudante + mentor) para desenvolvimento e revisão.

## Riscos e Mitigações
- **Dados insuficientes ou ruidosos** — Mitigação: análises de qualidade, imputação responsável, reduzir escopo do alvo.
- **Dados não estacionários** (mudanças de comportamento) — Mitigação: usar janelas móveis e validação temporal.
- **Privacidade** — Mitigação: anonimizar identificadores pessoais antes de compartilhar resultados.

## Métrica de Sucesso
- Modelo com erro aceitável definido pelo time (ex.: RMSE abaixo de X ou Pontuação de Acerto > 50%).
- Chatbot capaz de responder perguntas comuns sobre o modelo e gerar predições a partir de novos dados.
- Deploy funcional na Streamlit Cloud com documentação clara.

## Observação Didática
Esse PMC serve como mapa inicial: conecta contexto, problema e solução à implementação prática. Deve ser usado como referência ao iniciar os notebooks e os módulos no `src/`. Ajustes são esperados conforme a exploração dos dados.
