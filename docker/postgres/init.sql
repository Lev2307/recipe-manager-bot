CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    user_id BIGINT NOT NULL UNIQUE, 
    username VARCHAR(255), 
    offset_for_searching INTEGER DEFAULT 0,
    reg_date TIME WITHOUT TIME ZONE DEFAULT NOW()
);
CREATE TABLE favourites (
    id SERIAL PRIMARY KEY, 
    fav_user_id BIGINT NOT NULL, 
    api_recipe_id INTEGER NOT NULL, 
    title VARCHAR(255), 
    added_at TIME WITHOUT TIME ZONE, 
    FOREIGN KEY (fav_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);