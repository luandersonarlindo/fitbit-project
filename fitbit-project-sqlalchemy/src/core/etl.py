import pandas as pd
from sqlalchemy import text, Engine

def load_csv_to_sor(engine: Engine, csv_path: str):
    """
    Carrega dados de um CSV para a tabela SOR, convertendo a data para o formato YYYY-MM-DD.
    """
    import os
    
    # Se for caminho relativo, converte para absoluto
    if not os.path.isabs(csv_path):
        csv_path = os.path.abspath(csv_path)
    
    print(f"Carregando CSV de: {csv_path}")
    df = pd.read_csv(csv_path)

    # CORREÇÃO: Converte a coluna de data para o formato 'YYYY-MM-DD' usando Pandas
    # Isso é mais robusto do que manipular o texto dentro do SQL.
    # O format='%m/%d/%Y' ajuda o pandas a entender o formato de entrada.
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

    rename = {
        'Id':'user_id',
        'ActivityDate':'activity_date_txt',
        'TotalSteps':'total_steps',
        'TotalDistance':'total_distance',
        'TrackerDistance':'tracker_distance',
        'LoggedActivitiesDistance':'logged_activities_distance',
        'VeryActiveDistance':'very_active_distance',
        'ModeratelyActiveDistance':'moderately_active_distance',
        'LightActiveDistance':'light_active_distance',
        'SedentaryActiveDistance':'sedentary_active_distance',
        'VeryActiveMinutes':'very_active_minutes',
        'FairlyActiveMinutes':'fairly_active_minutes',
        'LightlyActiveMinutes':'lightly_active_minutes',
        'SedentaryMinutes':'sedentary_minutes',
        'Calories':'calories'
    }
    df = df.rename(columns=rename)
    df.to_sql("sor_daily_activity", engine, if_exists="append", index=False)


def transform_to_sot(engine: Engine):
    """
    Transforma dados da SOR para a SOT. A data já está no formato correto.
    """
    # A lógica complexa de data foi removida daqui, pois já foi tratada na função load_csv_to_sor
    sql = """
    INSERT INTO sot_daily_activity (
        user_id,
        activity_date,
        total_steps,
        total_distance,
        very_active_minutes,
        fairly_active_minutes,
        lightly_active_minutes,
        sedentary_minutes,
        calories
    )
    SELECT
        user_id,
        activity_date_txt,
        total_steps,
        total_distance,
        very_active_minutes,
        fairly_active_minutes,
        lightly_active_minutes,
        sedentary_minutes,
        calories
    FROM
        sor_daily_activity;
    """
    with engine.begin() as conn:
        conn.execute(text(sql))


def transform_to_spec(engine: Engine):
    """Transforma dados da SOT para a SPEC (Tabela Específica para o Modelo)."""
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO spec_activity_features (
                user_id, activity_date,
                total_steps, total_distance_km,
                mvpa_minutes, active_minutes,
                sedentary_minutes, calories, steps_per_km
            )
            SELECT
                user_id,
                activity_date,
                total_steps,
                total_distance AS total_distance_km,
                very_active_minutes + fairly_active_minutes AS mvpa_minutes,
                very_active_minutes + fairly_active_minutes + lightly_active_minutes AS active_minutes,
                sedentary_minutes,
                calories,
                CASE WHEN total_distance > 0 THEN total_steps / total_distance ELSE 0 END AS steps_per_km
            FROM sot_daily_activity
        """))

