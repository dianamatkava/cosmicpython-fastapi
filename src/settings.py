import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class AppSettings:
    BASE_APP_URL = os.getenv("BASE_APP_URL", "http://127.0.0.1:8000")
    DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/postgres")


def get_settings():
    return AppSettings()
