import os
import psycopg2
from dotenv import load_dotenv


def connect_to_db():
    load_dotenv()

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )

        print(f"Connected to '{dbname} successfully!")
        return conn

    except psycopg2.Error as e:
        print("Unable to connect to the '{dbname}")
        print(f"Error: {e}")
        return None
