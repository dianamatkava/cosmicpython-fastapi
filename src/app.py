from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import clear_mappers
from starlette import status

from src.allocations.adapters.orm import start_mappers
from src.allocations.routes.allocations import router as allocations_router
from src.allocations.routes.batchs import router as batch_router

app = FastAPI()
app.include_router(allocations_router)
app.include_router(batch_router)

router = APIRouter(prefix="")
app.include_router(router)


@router.get("/healthcheck", response_model=None, status_code=status.HTTP_200_OK)
def get_app_healthcheck():
    """Router to get all healthcheck."""


@app.on_event("startup")
def on_startup():
    clear_mappers()
    start_mappers()


@app.on_event("shutdown")
def on_shutdown():
    clear_mappers()
