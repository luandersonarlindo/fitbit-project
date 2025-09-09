CREATE TABLE IF NOT EXISTS sor_daily_activity (
    user_id INTEGER NOT NULL,
    activity_date_txt TEXT NOT NULL,
    total_steps INTEGER,
    total_distance REAL,
    tracker_distance REAL,
    logged_activities_distance REAL,
    very_active_distance REAL,
    moderately_active_distance REAL,
    light_active_distance REAL,
    sedentary_active_distance REAL,
    very_active_minutes INTEGER,
    fairly_active_minutes INTEGER,
    lightly_active_minutes INTEGER,
    sedentary_minutes INTEGER,
    calories INTEGER,
    PRIMARY KEY (user_id, activity_date_txt)
);