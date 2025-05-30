from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from src.adapters.orm import start_mappers
from src.routes.allocations import router as allocations_router
from src.routes.batch import router as batch_router

app = FastAPI()
app.include_router(allocations_router)
app.include_router(batch_router)


@app.on_event("startup")
def on_startup():
    clear_mappers()
    start_mappers()


@app.on_event("shutdown")
def on_shutdown():
    clear_mappers()
