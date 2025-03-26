import aiomysql
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# Muat variabel lingkungan dari file .env
load_dotenv()

# Konfigurasi koneksi MySQL dari variabel lingkungan
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
}


@asynccontextmanager
async def get_db_connection():
    """Mengelola koneksi database dengan context manager asynchronous."""
    connection = None
    try:
        connection = await aiomysql.connect(**DATABASE_CONFIG)
        yield connection
    except Exception as e:
        raise e
    finally:
        if connection:
            connection.close()
