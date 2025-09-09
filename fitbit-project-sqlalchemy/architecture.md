# Architecture

```mermaid
flowchart LR
    A[CSV: dailyActivity_merged.csv] -->|ingest| B[(SQLite DB)]
    subgraph DB
      B1[sor_daily_activity] --> B2[sot_daily_activity] --> B3[spec_activity_features]
    end
    B3 -->|train| C[Modelo: Linear Regression]
    C -->|save .pickle| D[(model/calories_regression.pickle)]
    E[main_app.py] -->|setup/teardown| DB
```
**Pipeline** (executado por `main_app.py`):
1. Cria o SQLite e as tabelas via `core/data/*.sql`  
2. Carrega o CSV para `SOR`  
3. Constrói `SOT` e `SPEC`  
4. Treina o modelo e salva `model/calories_regression.pickle`  
5. Dropa o database (remove o arquivo `.sqlite`)
