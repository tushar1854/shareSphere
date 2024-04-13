import psycopg2
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
# dbname = "fileshare"
# user = "postgres"
# password = "saini@123"
# host = "localhost"
# port = "5432"

# dbname = os.getenv("DB_NAME")
# user = os.getenv("UP_USER")
# password = os.getenv("PASSWORD")
# # host = os.getenv("HOST")
# # port = os.getenv("PORT")
# host = os.getenv("POSTGRES_HOST")  # Use the service name from Docker Compose
# port = os.getenv("POSTGRES_PORT")


def connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="rn7e7iYdNj5sjJyj5p6Y",
            host="database-2.cdi2sowk2z0j.us-east-1.rds.amazonaws.com",
            port=5432
        )
        return conn
    except Exception as e:
        return f"Error: {e}"
