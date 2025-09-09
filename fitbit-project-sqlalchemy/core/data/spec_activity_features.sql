CREATE TABLE IF NOT EXISTS spec_activity_features (
    user_id INTEGER NOT NULL,
    activity_date DATE NOT NULL,
    total_steps INTEGER,
    total_distance_km REAL,
    mvpa_minutes INTEGER, -- (very + fairly active)
    active_minutes INTEGER, -- (very + fairly + lightly active)
    sedentary_minutes INTEGER,
    calories INTEGER,
    steps_per_km REAL
);