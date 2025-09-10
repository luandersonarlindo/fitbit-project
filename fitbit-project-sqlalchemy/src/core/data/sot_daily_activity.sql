CREATE TABLE IF NOT EXISTS sot_daily_activity (
    user_id INTEGER NOT NULL,
    activity_date DATE NOT NULL,
    total_steps INTEGER,
    total_distance REAL,
    very_active_minutes INTEGER,
    fairly_active_minutes INTEGER,
    lightly_active_minutes INTEGER,
    sedentary_minutes INTEGER,
    calories INTEGER,
    PRIMARY KEY (user_id, activity_date)
);