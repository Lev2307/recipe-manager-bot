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
            WHERE tablename = %s
        );
    """
    cursor.execute(query, (table_name, ))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists