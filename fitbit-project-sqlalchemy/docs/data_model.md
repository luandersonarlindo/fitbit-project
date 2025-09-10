# 📊 Modelo de Dados - Fitbit Daily Activity

> **📚 Documentação Completa**: Veja o [README.md](README.md) para informações detalhadas sobre instalação e uso.

## 🎯 Arquitetura em Camadas

Este projeto implementa uma **arquitetura de dados em três zonas**:

- **🗄️ SOR (System of Record)**: Dados brutos do CSV original
- **✅ SOT (Source of Truth)**: Dados limpos e padronizados  
- **🤖 SPEC (Model Spec)**: Features prontas para Machine Learning

## Tabelas

### SOR — `sor_daily_activity`
**Grão**: 1 linha por (`user_id`, `activity_date`).  
**Descrição**: Cópia fiel do CSV `dailyActivity_merged.csv` (colunas e semântica originais).  
**Colunas**:
- `user_id` (INTEGER) – mapeia `Id`
- `activity_date_txt` (TEXT) – mapeia `ActivityDate` (texto original)
- `total_steps` (INTEGER)
- `total_distance` (REAL)
- `tracker_distance` (REAL)
- `logged_activities_distance` (REAL)
- `very_active_distance` (REAL)
- `moderately_active_distance` (REAL)
- `light_active_distance` (REAL)
- `sedentary_active_distance` (REAL)
- `very_active_minutes` (INTEGER)
- `fairly_active_minutes` (INTEGER)
- `lightly_active_minutes` (INTEGER)
- `sedentary_minutes` (INTEGER)
- `calories` (INTEGER)

**Chave primária**: (`user_id`, `activity_date_txt`).

### SOT — `sot_daily_activity`
**Grão**: 1 linha por (`user_id`, `activity_date`).  
**Descrição**: Conversão de tipos e padronização de data + métricas derivadas simples.
**Colunas**:
- `user_id` (INTEGER)
- `activity_date` (DATE) – `YYYY-MM-DD`
- `total_steps` (INTEGER)
- `total_distance_km` (REAL)
- `mvpa_minutes` (INTEGER) – *Moderate-to-Vigorous Physical Activity* = `very_active_minutes + fairly_active_minutes`
- `active_minutes` (INTEGER) – `very + fairly + lightly`
- `sedentary_minutes` (INTEGER)
- `steps_per_km` (REAL) – `CASE WHEN total_distance_km>0 THEN total_steps/total_distance_km END`
- `calories` (INTEGER)

**Chave primária**: (`user_id`, `activity_date`).

### SPEC — `spec_activity_features`
**Grão**: 1 linha por (`user_id`, `activity_date`).  
**Uso**: *features* para predição de `calories` (modelo de regressão).
**Colunas**:
- `user_id` (INTEGER)
- `activity_date` (DATE)
- `total_steps` (INTEGER)
- `total_distance_km` (REAL)
- `mvpa_minutes` (INTEGER)
- `active_minutes` (INTEGER)
- `sedentary_minutes` (INTEGER)
- `steps_per_km` (REAL)
- `calories` (INTEGER) — *label*
- `set_type` (TEXT) — 'train' | 'valid' | 'test' (divisão temporal simples)

**Particionamento sugerido**: divisão temporal 70/15/15 conforme data.

