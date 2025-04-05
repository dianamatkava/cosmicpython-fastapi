import os

from fastapi import FastAPI

from src.conf import create_db_and_tables
from src.routes.allocations import router as allocations_router

app = FastAPI()
app.include_router(allocations_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class AppSettings:
    BASE_APP_URL = os.getenv("BASE_APP_URL", "http://127.0.0.1:8000")


def get_settings():
    return AppSettings()
