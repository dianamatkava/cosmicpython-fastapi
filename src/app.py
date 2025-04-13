from fastapi import FastAPI

from src.adapters.orm import start_mappers
from src.routes.allocations import router as allocations_router

app = FastAPI()
app.include_router(allocations_router)


@app.on_event("startup")
def on_startup():
    # Initializes the mapping between domain models and the database tables.
    start_mappers()
