ALTER ROLE ALL SET TIME ZONE 'Europe/Moscow';

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    user_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(255), 
    offset_for_searching INTEGER DEFAULT 1,
    is_sub BOOLEAN DEFAULT TRUE, 
    last_search_request_time TIMESTAMP WITH TIME ZONE,
    count_requests_per_day INTEGER DEFAULT 0,
    reg_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);
CREATE TABLE favourites (
    id SERIAL PRIMARY KEY, 
    fav_user_id BIGINT NOT NULL, 
    api_recipe_id INTEGER NOT NULL, 
    added_at TIMESTAMP WITH TIME ZONE, 
    FOREIGN KEY (fav_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);