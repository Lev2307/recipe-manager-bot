CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER NOT NULL UNIQUE, 
    username VARCHAR(255), 
    reg_date TIME WITHOUT TIME ZONE
);
CREATE TABLE favourites (
    id SERIAL PRIMARY KEY, 
    fav_user_id INTEGER NOT NULL, 
    api_recipe_id INTEGER NOT NULL, 
    title VARCHAR(255), 
    added_at TIME WITHOUT TIME ZONE, 
    FOREIGN KEY (fav_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);