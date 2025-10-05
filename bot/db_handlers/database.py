from datetime import datetime, timedelta
import os
import pytz

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def generate_fav_recipe_data(favourite_recipe: tuple):
    return {
            'id': favourite_recipe[0],
            'fav_user_id': favourite_recipe[1],
            'api_recipe_id': favourite_recipe[2],
            'added_at': favourite_recipe[3],
        }

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_NAME"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=int(os.environ.get("POSTGRES_PORT"))
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to db: {e}")

def table_exists(conn, table_name: str):
    cursor = conn.cursor()
    query = """
        SELECT EXISTS(
            SELECT FROM pg_tables
            WHERE tablename = %s;
        );
    """
    cursor.execute(query, (table_name, ))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists

def get_user(conn, user_id: int):
    """ Checks if user with passed user_id exists in db """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=%s;", (user_id, ))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return {
            'id': user[0],
            'user_id': user[1],
            'username': user[2],
            'last_search_request_time': user[3],
            'offset_for_searching': user[4],
            'reg_date': user[5]
        }
    return user

def create_user(conn, user_id, username):
    """ Creates user instance in db """
    five_minutes_earlier_time = datetime.now(pytz.timezone('Europe/Moscow')) + timedelta(minutes=-5)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id, username, last_search_request_time) VALUES (%s, %s, %s);", (user_id, username, five_minutes_earlier_time))
    conn.commit()
    cur.close()
    
def modify_user_offset(conn, user_id: int, old_offset: int):
    """ Modifies offset_for_searching field increasing it by 1 or rather zeroing it out when offset gets more than 900 """
    new_offset = 0
    if (old_offset + 1) <= 900:
        new_offset = old_offset + 1
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE users
            SET offset_for_searching=%s
            WHERE user_id=%s;
        """, 
        (new_offset, user_id)
    )
    conn.commit()
    cursor.close()

def modify_last_search_request_time(conn, user_id: int, new_time: datetime):
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE users
            SET last_search_request_time=%s
            WHERE user_id=%s;
        """,
        (new_time, user_id))
    conn.commit()
    cursor.close()

def add_favourite_recipe_to_user(conn, user_id: int, recipe_id: int, added_at: datetime):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO favourites (fav_user_id, api_recipe_id, added_at) VALUES (%s, %s, %s);", (user_id, recipe_id, added_at))
    conn.commit()
    cursor.close()

def delete_recipe_from_favourites(conn, user_id: int, recipe_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favourites WHERE fav_user_id=%s AND api_recipe_id=%s", (user_id, recipe_id))
    conn.commit()
    cursor.close()

def get_favourite_recipe(conn, user_id: int, recipe_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favourites WHERE fav_user_id=%s AND api_recipe_id=%s;", (user_id, recipe_id))
    fav = cursor.fetchone()
    cursor.close()
    if fav:
        return generate_fav_recipe_data(fav)
    return fav

def get_favourites(conn, user_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM favourites WHERE fav_user_id=%s
        ORDER BY added_at;
    """, (user_id, ))
    favourites = cursor.fetchall()
    cursor.close()
    return [generate_fav_recipe_data(fav) for fav in favourites]