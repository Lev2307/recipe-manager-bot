import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

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
    return user

def create_user(conn, user_id, username):
    """ Creates user instance in db """
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id, username) VALUES (%s, %s);", (user_id, username))
    conn.commit()
    cur.close()
    
def modify_user_offset(conn, user_id: int, old_offset: int):
    """ Modifies offset_for_searching field increasing it by 1 or rather zeroing it out when offset gets more than 900 """
    new_offset = 0
    if (old_offset + 1) <= 900:
        new_offset = old_offset + 1
        print(new_offset)
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE users
            SET offset_for_searching=%s
            WHERE user_id=%s;
        """, 
        (new_offset, user_id)
    )
    cursor.close()