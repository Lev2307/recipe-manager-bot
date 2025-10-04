ALTER ROLE ALL SET TIME ZONE 'Europe/Moscow';

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    user_id BIGINT NOT NULL UNIQUE, 
    username VARCHAR(255), 
    offset_for_searching INTEGER DEFAULT 10,
    reg_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE favourites (
    id SERIAL PRIMARY KEY, 
    fav_user_id BIGINT NOT NULL, 
    api_recipe_id INTEGER NOT NULL, 
    added_at TIMESTAMP WITH TIME ZONE, 
    FOREIGN KEY (fav_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);